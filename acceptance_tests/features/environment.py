import logging
import time
from datetime import datetime
from distutils.util import strtobool

import requests
from behave import register_type
from structlog import wrap_logger

from acceptance_tests.utilities.audit_trail_helper import log_out_user_context_values
from acceptance_tests.utilities.exception_manager_helper import get_bad_messages, \
    quarantine_bad_messages_check_and_reset
from acceptance_tests.utilities.pubsub_helper import purge_outbound_topics
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

logger = wrap_logger(logging.getLogger(__name__))

register_type(boolean=lambda text: strtobool(text))


def purge_fulfilment_triggers():
    response = requests.get(f'{Config.SUPPORT_TOOL_API}/fulfilmentNextTriggers')
    response.raise_for_status()

    trigger_items = response.json()['_embedded']['fulfilmentNextTriggers']

    for trigger_item in trigger_items:
        trigger_id = trigger_item['_links']['self']['href'].split("/")[-1]
        url = f'{Config.SUPPORT_TOOL_API}/fulfilmentNextTriggers/{trigger_id}'

        delete_response = requests.delete(url)
        delete_response.raise_for_status()


def before_all(_context):
    logging.getLogger("pika").setLevel(logging.WARNING)


def before_scenario(context, scenario):
    purge_outbound_topics()
    purge_fulfilment_triggers()

    context.test_start_local_datetime = datetime.now()
    context.correlation_id = None
    context.originating_user = None
    context.sent_messages = []
    context.scenario_name = scenario


def after_all(_context):
    purge_outbound_topics()
    purge_fulfilment_triggers()


def after_scenario(context, scenario):
    if getattr(scenario, 'status') == 'failed':
        log_out_user_context_values(context)

    unexpected_bad_messages = get_bad_messages()

    if unexpected_bad_messages:
        _record_and_remove_any_unexpected_bad_messages(unexpected_bad_messages)


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
