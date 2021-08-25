import hashlib
import time
import uuid

import requests
from behave import step

from acceptance_tests.utilities.exception_manager_helper import quarantine_bad_messages
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


ALL_INCOMING_TOPICS = [Config.PUBSUB_RECEIPT_TOPIC, Config.PUBSUB_REFUSAL_TOPIC, Config.PUBSUB_INVALID_CASE_TOPIC,
                       Config.PUBSUB_DEACTIVATE_UAC_TOPIC, Config.PUBSUB_PRINT_FULFILMENT_TOPIC,
                       Config.PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC, Config.PUBSUB_UAC_AUTHENTICATION_TOPIC]


@step("a bad json msg is sent to every topic consumed by RM")
def put_a_bad_msg_on_every_topic_on(context):
    context.message_hashes = []

    for topic in ALL_INCOMING_TOPICS:
        message = 'not even close to json' + str(uuid.uuid4())

        publish_to_pubsub(message,
                          Config.PUBSUB_PROJECT,
                          topic)

        context.message_hashes.append(hashlib.sha256(message.encode('utf-8')).hexdigest())


@step('each bad msg is seen by exception manager with the message containing "{expected_exception_msg}"')
def look_for_each_bad_msg(context, expected_exception_msg):
    time.sleep(5)
    response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessages/summary')
    response.raise_for_status()
    bad_messages = response.json()

    test_helper.assertEqual(len(bad_messages), len(context.message_hashes),
                            msg='actual number of bad msgs does not match expected number of hashes')

    for bad_message in bad_messages:
        test_helper.assertGreater(bad_message['seenCount'], 1,
                                  msg=f'Seen count is not greater than 1, failed bad message summary: {bad_message}')

        test_helper.assertIn(bad_message['messageHash'], context.message_hashes,
                             msg=f'Unknown bad message hash, message summary: {bad_message}')

        _check_message_exception_as_expected(bad_message['messageHash'], expected_exception_msg)


def _check_message_exception_as_expected(bad_message_hash, expected_exception):
    response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessage/{bad_message_hash}')
    response.raise_for_status()
    message_details = response.json()

    test_helper.assertIn(expected_exception, message_details[0]['exceptionReport']['exceptionMessage'],
                         msg='Execption manager exception messsge differs from expected message')


@step('a bad message appears in exception manager with exception message containing "{expected_exception_msg}"')
def bad_message_appears_in_exception_manager(context, expected_exception_msg):
    look_for_each_bad_msg(context, expected_exception_msg)


@step("each bad msg can be successfully quarantined")
def each_bad_msg_can_be_successfully_quarantined(context):
    quarantine_bad_messages(context.message_hashes)

    # test locally this was enough time for the reset messages to re appear, leaving it longer would be 'better'
    # to check that quarantine has worked, but for example 30 seconds would slow the tests hugely
    time.sleep(3)

    response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessages/summary')
    response.raise_for_status()
    bad_messages = response.json()

    test_helper.assertEqual(len(bad_messages), 0, msg=f'Zero bad messages were expected. Received {len(bad_messages)}')
