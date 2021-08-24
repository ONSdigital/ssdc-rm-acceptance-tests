import logging
import time
from datetime import datetime
from distutils.util import strtobool

import requests
from behave import register_type
from structlog import wrap_logger

from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.exception_manager_helper import get_bad_messages_and_clear
from acceptance_tests.utilities.pubsub_helper import purge_outbound_topics
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

logger = wrap_logger(logging.getLogger(__name__))

register_type(boolean=lambda text: strtobool(text))


def purge_fulfilment_triggers():
    with open_cursor() as cur:
        delete_trigger_query = """DELETE FROM casev3.fulfilment_next_trigger"""
        cur.execute(delete_trigger_query)


def before_all(_context):
    logging.getLogger("pika").setLevel(logging.WARNING)


def before_scenario(context, _):
    # TODO - this is a hack and should be removed/refactored when we understand better what's going on
    time.sleep(2)

    purge_outbound_topics()
    purge_fulfilment_triggers()

    context.test_start_local_datetime = datetime.now()


def after_all(_context):
    purge_outbound_topics()
    purge_fulfilment_triggers()


def after_scenario(_, _scenario):
    response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessages')
    response.raise_for_status()

    if response.json():
        logger.error('Unexpected exception(s) -- these could be due to an underpowered environment',
                     exception_manager_response=response.json())

        requests.get(f'{Config.EXCEPTION_MANAGER_URL}/reset')
        time.sleep(25)  # 25 seconds should be long enough for error to happen again if it hasn't cleared itself

        response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessages')
        response.raise_for_status()
        if response.json():
            bad_message_details = []

            list_of_bad_message_hashes = response.json()
            for bad_message_hash in list_of_bad_message_hashes:
                response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessage/{bad_message_hash}')
                bad_message_details.append(response.json())

            _clear_queues_for_bad_messages_and_reset_exception_manager()
            logger.error('Unexpected exception(s) which were not due to eventual consistency timing',
                         exception_manager_response=bad_message_details)

            test_helper.fail(f'Unexpected exception(s) thrown by RM. Details: {bad_message_details}')


def _clear_queues_for_bad_messages_and_reset_exception_manager():
    for _ in range(4):
        purge_outbound_topics()
        get_bad_messages_and_clear()
        time.sleep(1)

    time.sleep(5)
    requests.get(f'{Config.EXCEPTION_MANAGER_URL}/reset')
