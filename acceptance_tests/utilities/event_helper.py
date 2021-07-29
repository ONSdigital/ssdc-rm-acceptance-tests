import functools
import json

from google.cloud import pubsub_v1

from acceptance_tests.utilities.rabbit_helper import start_listening_to_rabbit_queue, store_in_message_list
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_emitted_cases(type_filter, expected_msg_count=1):
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=expected_msg_count,
                                           type_filter=type_filter)

    test_helper.assertEqual(len(messages_received), expected_msg_count,
                            f'Did not find expected number of events, type: {type_filter}')

    case_payloads = [message_received['payload']['collectionCase'] for message_received in messages_received]

    return case_payloads


def start_listening_to_pubsub_subscription(subscription, expected_msg_count, message_list, type_filter):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(Config.PUBSUB_PROJECT,
                                                     subscription)
    response = subscriber.pull(subscription_path, max_messages=expected_msg_count, timeout=30)

    ack_ids = []

    for received_message in response.received_messages:
        parsed_body = json.loads(received_message.message.data)
        if type_filter is None or parsed_body['event']['type'] == type_filter:
            message_list.append(parsed_body)
            ack_ids.append(received_message.ack_id)
        else:
            # take it, ignore it?
            assert False

    if ack_ids:
        subscriber.acknowledge(subscription_path, ack_ids)

    subscriber.close()


def get_emitted_case_update():
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=1,
                                           type_filter='CASE_UPDATED')

    test_helper.assertEqual(len(messages_received), 1, 'Expected to receive one and only one CASE_UPDATED message')

    return messages_received[0]['payload']['collectionCase']


def get_emitted_uac_update():
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=1,
                                           type_filter='UAC_UPDATED')

    test_helper.assertEqual(len(messages_received), 1, 'Expected to receive one and only one UAC_UPDATED message')

    return messages_received[0]['payload']['uac']


def get_uac_updated_events(expected_number):
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=expected_number,
                                           type_filter='UAC_UPDATED')

    uac_payloads = [uac_event['payload']['uac'] for uac_event in messages_received]
    return uac_payloads
