import functools

from behave import step

from acceptance_tests.utilities.event_helper import get_emitted_case, get_emitted_uac, get_uac_updated_events
from acceptance_tests.utilities.rabbit_helper import start_listening_to_rabbit_queue, store_all_msgs_in_list
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("a uac_updated msg is emitted with active set to false")
def uac_updated_msg_emitted(context):
    emitted_uac = get_emitted_uac()
    test_helper.assertEqual(emitted_uac['caseId'], context.emitted_cases_id[0])
    test_helper.assertFalse(emitted_uac['active'], 'The UAC_UPDATED message should active flag "false"')


@step('a case_updated msg is emitted where "{case_field}" is "{expected_field_value}"')
def case_updated_msg_sent_with_values(context, case_field, expected_field_value):
    emitted_case = get_emitted_case()

    test_helper.assertEqual(emitted_case['caseId'], context.uac_created_events[0]['payload']['uac']['caseId'])
    test_helper.assertEqual(str(emitted_case[case_field]), expected_field_value)


@step("uac_updated msgs are emitted with active set to true")
def check_uac_updated_msgs_emitted_with_qid_active(context):
    context.uac_created_events = get_uac_updated_events(context, len(context.emitted_cases))
    _check_uacs_updated_match_cases(context.uac_created_events, context.emitted_cases_id)

    for uac in context.uac_created_events:
        test_helper.assertTrue(uac['payload']['uac']['active'], f'Newly created UAC QID pairs should be active,'
                                                                f' QID: {uac["payload"]["uac"]["questionnaireId"]}')


def _check_uacs_updated_match_cases(uac_updated_events, case_ids):
    test_helper.assertSetEqual(set(uac['payload']['uac']['caseId'] for uac in uac_updated_events),
                               set(case_ids))

    test_helper.assertEqual(len(uac_updated_events), len(case_ids))


def get_emitted_cases(type_filter, expected_msg_count=1):
    messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_CASE_QUEUE,
                                    functools.partial(
                                        store_all_msgs_in_list, message_list=messages_received,
                                        expected_msg_count=expected_msg_count,
                                        type_filter=type_filter))

    test_helper.assertEqual(len(messages_received), expected_msg_count,
                            f'Did not find expected number of events, type: {type_filter}')

    case_payloads = [message_received['payload']['collectionCase'] for message_received in messages_received]

    return case_payloads


