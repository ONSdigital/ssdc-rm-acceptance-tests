from typing import Mapping

import requests
from behave import step
from tenacity import retry, wait_fixed, stop_after_delay

from acceptance_tests.utilities.jwe_helper import decrypt_signed_jwe
from acceptance_tests.utilities.pubsub_helper import get_matching_pubsub_message_acking_others
from acceptance_tests.utilities.test_case_helper import test_helper
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
                                                                   _message_matcher, context.test_start_utc_datetime)

    test_helper.assertIsNotNone(cloud_task_message['payload'].get('transactionId'),
                                'Expected EQ flush cloud task payload to have a transaction ID')


@step('the EQ flush endpoint is called with the token for flushing the correct QIDs partial')
def check_eq_stub_flush_call_log(context):
    flush_call = poll_for_one_eq_stub_flush_call()

    context.eq_flush_claims = decrypt_signed_jwe(flush_call['token'])

    test_helper.assertTrue(context.eq_flush_claims['response_id'].startswith(context.emitted_uacs[0]['qid']),
                           'Flush response ID should start with the correct QID')
    test_helper.assertIsNotNone(context.eq_flush_claims['tx_id'], 'tx_id must be set in the flushing claims')
    test_helper.assertEqual(context.eq_flush_claims['roles'], ['flusher'],
                            'The roles must be "flusher" in flushing claims')


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def poll_for_one_eq_stub_flush_call() -> Mapping:
    eq_stub_response = requests.get(f'{Config.EQ_FLUSH_STUB_URL}/log/flush')
    eq_stub_response.raise_for_status()
    eq_stub_log = eq_stub_response.json()

    test_helper.assertEqual(len(eq_stub_log), 1,
                            f'Expected exactly one EQ flush call to be logged, log: {eq_stub_log}')

    return eq_stub_log[0]


@step('the EQ flush claims response ID matches the EQ launch claims response ID')
def check_flush_and_launch_response_id_match(context):
    test_helper.assertEqual(context.eq_flush_claims['response_id'], context.eq_launch_claims['response_id'],
                            'The flush response ID must match the launch response ID ')
