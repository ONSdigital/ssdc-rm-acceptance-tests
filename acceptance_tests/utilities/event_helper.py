import json

from google.cloud import pubsub_v1

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_emitted_cases(expected_msg_count=1):
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=expected_msg_count)

    test_helper.assertEqual(len(messages_received), expected_msg_count,
                            'Did not find expected number of events')

    case_payloads = []
    for message_received in messages_received:
        test_helper.assertEqual(message_received['header']['originatingUser'], Config.SAMPLE_LOAD_ORIGINATING_USER,
                                'Unexpected originating user')
        case_payloads.append(message_received['payload']['caseUpdate'])

    return case_payloads


def start_listening_to_pubsub_subscription(subscription, expected_msg_count, message_list):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(Config.PUBSUB_PROJECT,
                                                     subscription)
    received_messages = _attempt_to_get_expected_number_of_messages(subscriber, subscription_path, expected_msg_count)

    ack_ids = []

    for received_message in received_messages:
        parsed_body = json.loads(received_message.message.data)
        message_list.append(parsed_body)
        ack_ids.append(received_message.ack_id)

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


def get_emitted_case_update(correlation_id, originating_user):
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=1)

    test_helper.assertEqual(len(messages_received), 1, 'Expected to receive one and only one CASE_UPDATE message')

    if correlation_id:
        test_helper.assertEqual(messages_received[0]['header']['correlationId'], correlation_id,
                                'Unexpected correlation ID')

    if originating_user:
        test_helper.assertEqual(messages_received[0]['header']['originatingUser'], originating_user,
                                'Unexpected originating user')

    return messages_received[0]['payload']['caseUpdate']


def get_emitted_uac_update(correlation_id, originating_user):
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=1)

    test_helper.assertEqual(len(messages_received), 1, 'Expected to receive one and only one UAC_UPDATE message')

    if correlation_id:
        test_helper.assertEqual(messages_received[0]['header']['correlationId'], correlation_id,
                                'Unexpected correlation ID')

    if originating_user:
        test_helper.assertEqual(messages_received[0]['header']['originatingUser'], originating_user,
                                'Unexpected originating user')

    return messages_received[0]['payload']['uacUpdate']


def get_uac_update_events(expected_number, correlation_id, originating_user):
    messages_received = []
    start_listening_to_pubsub_subscription(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                           message_list=messages_received,
                                           expected_msg_count=expected_number)
    uac_payloads = []
    for uac_event in messages_received:
        if correlation_id:
            test_helper.assertEqual(uac_event['header']['correlationId'], correlation_id,
                                    'Unexpected correlation ID')

        if originating_user:
            test_helper.assertEqual(uac_event['header']['originatingUser'], originating_user,
                                    'Unexpected originating user')

        uac_payloads.append(uac_event['payload']['uacUpdate'])

    return uac_payloads
