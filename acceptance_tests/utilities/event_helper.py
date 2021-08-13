import json

from google.cloud import pubsub_v1

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

    case_payloads = [message_received['payload']['caseUpdate'] for message_received in messages_received]

    return case_payloads


def start_listening_to_pubsub_subscription(subscription, expected_msg_count, message_list, type_filter):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(Config.PUBSUB_PROJECT,
                                                     subscription)
    received_messages = _attempt_to_get_expected_number_of_messages(subscriber, subscription_path, expected_msg_count)

    ack_ids = []

    for received_message in received_messages:
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


def _attempt_to_get_expected_number_of_messages(subscriber, subscription_path, expected_msg_count):
    messages = []
    remaining_messages_to_get = expected_msg_count
    last_one = False

    while remaining_messages_to_get and not last_one:
        if remaining_messages_to_get == 1:
            last_one = True

        response = subscriber.pull(subscription_path, max_messages=remaining_messages_to_get, timeout=30)

        messages += response.received_messages
        remaining_messages_to_get -= len(response.received_messages)

    return messages


def get_emitted_case_update():
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=1,
                                           type_filter='CASE_UPDATE')

    test_helper.assertEqual(len(messages_received), 1, 'Expected to receive one and only one CASE_UPDATE message')

    return messages_received[0]['payload']['caseUpdate']


def get_emitted_uac_update():
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=1,
                                           type_filter='UAC_UPDATE')

    test_helper.assertEqual(len(messages_received), 1, 'Expected to receive one and only one UAC_UPDATE message')

    return messages_received[0]['payload']['uacUpdate']


def get_uac_update_events(expected_number):
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=expected_number,
                                           type_filter='UAC_UPDATE')

    uac_payloads = [uac_event['payload']['uacUpdate'] for uac_event in messages_received]
    return uac_payloads
