from datetime import time

import requests
from behave import *

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

use_step_matcher("re")

ALL_INCOMING_TOPICS = [Config.PUBSUB_RECEIPT_TOPIC, Config.PUBSUB_REFUSAL_TOPIC, Config.PUBSUB_INVALID_CASE_TOPIC,
                       Config.PUBSUB_DEACTIVATE_UAC_TOPIC, Config.PUBSUB_PRINT_FULFILMENT_TOPIC,
                       Config.PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC, Config.PUBSUB_UAC_AUTHENTICATION_TOPIC]


@when("a bad json msg is sent to every topic consumed by RM")
def put_a_bad_msg_on_every_topic_on(context):
    message = 'not even close to json'

    for topic in ALL_INCOMING_TOPICS:
        publish_to_pubsub(message,
                          Config.PUBSUB_PROJECT,
                          topic)


@then("each bad msg is seen by exception manager")
def look_for_each_bad_msg(context):
    time.sleep(30)
    response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessages/summary')
    bad_messages = response.json()

    for bad_message in bad_messages:
        test_helper.assertGreater(bad_message['seenCount'], 1,
                                  msg=f'Seen count is not greater than 1, failed bad message summary: {bad_message}')
        test_helper.assertIn(bad_message['messageHash'], context.message_hashes,
                             msg=f'Unknown bad message hash, message summary: {bad_message}')
