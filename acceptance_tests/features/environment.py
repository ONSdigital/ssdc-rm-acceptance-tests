import logging
import time
from datetime import datetime
from distutils.util import strtobool

import behave_webdriver
import requests
from behave import register_type
from structlog import wrap_logger

from acceptance_tests.utilities.audit_trail_helper import log_out_user_context_values, parse_markdown_context_table
from acceptance_tests.utilities.exception_manager_helper import get_bad_messages, \
    quarantine_bad_messages_check_and_reset
from acceptance_tests.utilities.notify_helper import reset_notify_stub
from acceptance_tests.utilities.parameter_parsers import parse_array_to_list, parse_json_object
from acceptance_tests.utilities.pubsub_helper import purge_outbound_topics
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config
from selenium import webdriver

logger = wrap_logger(logging.getLogger(__name__))

register_type(boolean=strtobool)
register_type(json=parse_json_object)
register_type(array=parse_array_to_list)

CONTEXT_ATTRIBUTES = parse_markdown_context_table(Config.CODE_GUIDE_MARKDOWN_FILE_PATH)


def before_all(context):
    context.config.setup_logging()


def move_fulfilment_triggers_harmlessly_massively_into_the_future():
    # The year 3000 ought to be far enough in the future for this fulfilment to never trigger again, no?
    url = f'{Config.SUPPORT_TOOL_API}/fulfilmentNextTriggers/?triggerDateTime=3000-01-01T00:00:00.000Z'

    response = requests.post(url)
    response.raise_for_status()


def before_scenario(context, scenario):
    purge_outbound_topics()
    move_fulfilment_triggers_harmlessly_massively_into_the_future()

    context.test_start_utc_datetime = datetime.utcnow()
    context.correlation_id = None
    context.originating_user = None
    context.sent_messages = []
    context.scenario_name = scenario

    if "reset_notify_stub" in scenario.tags:
        reset_notify_stub()

    if 'web' in context.tags:
        # if headless: etc
        context.behave_driver = behave_webdriver.Chrome.headless(executable_path='/Users/lozel/Downloads/chromedriver')
        context.behave_driver.implicitly_wait(10)


def after_all(_context):
    purge_outbound_topics()
    move_fulfilment_triggers_harmlessly_massively_into_the_future()


def after_scenario(context, scenario):
    if getattr(scenario, 'status') == 'failed':
        log_out_user_context_values(context, CONTEXT_ATTRIBUTES)

    unexpected_bad_messages = get_bad_messages()

    if unexpected_bad_messages:
        _record_and_remove_any_unexpected_bad_messages(unexpected_bad_messages)

    if 'web' in context.tags:
        context.behave_driver.quit()


def _record_and_remove_any_unexpected_bad_messages(unexpected_bad_messages):
    logger.error('Unexpected exception(s) -- these could be due to an underpowered environment',
                 exception_manager_response=unexpected_bad_messages)

    requests.get(f'{Config.EXCEPTION_MANAGER_URL}/reset')
    time.sleep(25)  # 25 seconds should be long enough for error to happen again if it hasn't cleared itself

    list_of_bad_message_hashes = get_bad_messages()

    if list_of_bad_message_hashes:
        bad_message_details = []

        for bad_message_hash in list_of_bad_message_hashes:
            response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessage/{bad_message_hash}')
            response.raise_for_status()
            bad_message_details.append(response.json())

        _clear_queues_for_bad_messages_and_reset_exception_manager(list_of_bad_message_hashes)
        logger.error('Unexpected exception(s) which were not due to eventual consistency timing',
                     exception_manager_response=bad_message_details)

        test_helper.fail(f'Unexpected exception(s) thrown by RM. Details: {bad_message_details}')


def _clear_queues_for_bad_messages_and_reset_exception_manager(list_of_bad_message_hashes):
    for _ in range(4):
        purge_outbound_topics()
        time.sleep(1)

    quarantine_bad_messages_check_and_reset(list_of_bad_message_hashes)
