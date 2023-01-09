import time
from typing import Mapping

import requests
from behave import step

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
                                                                   _message_matcher)

    assert cloud_task_message['payload'].get('transactionId') is not None, \
        'Expect EQ flush cloud task payload to have a transaction ID'


@step('the eQ flush endpoint is called with the token for flushing the correct QIDs partial')
def check_eq_stub_flush_call_log(context):
    timeout = time.time() + 30  # Allow time for the calls
    while time.time() < timeout:
        eq_stub_response = requests.get(f'{Config.EQ_FLUSH_STUB_URL}/log/flush')
        eq_stub_response.raise_for_status()
        eq_stub_log = eq_stub_response.json()

        if len(eq_stub_log) > 1:
            test_helper.fail(
                f'Found multiple calls in the eq stub call log when only one is expected, call log: {eq_stub_log}')
        if not eq_stub_log:
            time.sleep(0.5)
            continue
        eq_stub_call = eq_stub_log[0]
        flush_token = eq_stub_call['token']
        break
    else:
        test_helper.fail('Timed out waiting for eq stub call')

    token_contents = decrypt_signed_jwe(flush_token)

    test_helper.assertTrue(token_contents['response_id'].startswith(context.emitted_uacs[0]['qid']),
                           'Flush response ID should start with the correct QID')
    test_helper.assertIsNotNone(token_contents['tx_id'], 'tx_id must be set in the flushing claims')
    test_helper.assertEqual(token_contents['roles'], ['flusher'], 'The roles must be "flusher" in flushing claims')
