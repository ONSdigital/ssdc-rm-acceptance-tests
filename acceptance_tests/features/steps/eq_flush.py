from typing import Mapping

from behave import step

from acceptance_tests.utilities.pubsub_helper import get_matching_pubsub_message_acking_others
from config import Config


@step("an EQ_FLUSH cloud task queue message is sent for the correct QID")
def check_eq_flush_cloud_task_message(context):
    def _message_matcher(message: Mapping) -> tuple[bool, str]:
        if message['cloudTaskType'] != 'EQ_FLUSH':
            return False, f'Found message with incorrect cloudTaskType: {message["cloudTaskType"]}'
        elif message['payload']['qid'] != context.emitted_uacs[0]['qid']:
            return False, f'Found message with incorrect qid: {message["payload"]["qid"]}'
        return True, ''
    cloud_task_message = get_matching_pubsub_message_acking_others(Config.PUBSUB_CLOUD_TASK_QUEUE_AT_SUBSCRIPTION,
                                                                   _message_matcher)

    assert cloud_task_message['payload'].get('transactionId') is not None, \
        'Expect EQ flush cloud task payload to have a transaction ID'
