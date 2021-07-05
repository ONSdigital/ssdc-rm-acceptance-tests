import functools

from acceptance_tests.utilities.rabbit_helper import start_listening_to_rabbit_queue, store_in_message_list
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_emitted_cases(type_filter, expected_msg_count=1):
    messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_CASE_QUEUE,
                                    functools.partial(
                                        store_in_message_list,
                                        message_list=messages_received,
                                        expected_msg_count=expected_msg_count,
                                        type_filter=type_filter))

    test_helper.assertEqual(len(messages_received), expected_msg_count,
                            f'Did not find expected number of events, type: {type_filter}')

    case_payloads = [message_received['payload']['collectionCase'] for message_received in messages_received]

    return case_payloads


def get_emitted_case_update():
    messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_CASE_QUEUE,
                                    functools.partial(
                                        store_in_message_list,
                                        message_list=messages_received,
                                        expected_msg_count=1,
                                        type_filter='CASE_UPDATED'))

    test_helper.assertEqual(len(messages_received), 1, 'Expected to receive one and only one CASE_UPDATED message')

    return messages_received[0]['payload']['collectionCase']


def get_emitted_uac_update():
    messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE,
                                    functools.partial(
                                        store_in_message_list,
                                        message_list=messages_received,
                                        expected_msg_count=1,
                                        type_filter='UAC_UPDATED'))

    test_helper.assertEqual(len(messages_received), 1, 'Expected to receive one and only one UAC_UPDATED message')

    return messages_received[0]['payload']['uac']


def get_uac_updated_events(expected_number):
    messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE,
                                    functools.partial(store_in_message_list,
                                                      message_list=messages_received,
                                                      expected_msg_count=expected_number,
                                                      type_filter='UAC_UPDATED'))
    uac_payloads = [uac_event['payload']['uac'] for uac_event in messages_received]
    return uac_payloads
