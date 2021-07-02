from behave import step

from acceptance_tests.utilities.event_helper import get_emitted_case, get_emitted_uac, get_uac_updated_events
from acceptance_tests.utilities.test_case_helper import test_helper


@step("a UAC_UPDATED message is emitted with active set to false")
def uac_updated_msg_emitted(context):
    emitted_uac = get_emitted_uac()
    test_helper.assertEqual(emitted_uac['caseId'], context.emitted_cases_id[0])
    test_helper.assertFalse(emitted_uac['active'], 'The UAC_UPDATED message should active flag "false"')


@step('a CASE_UPDATED message is emitted where "{case_field}" is "{expected_field_value}"')
def case_updated_msg_sent_with_values(context, case_field, expected_field_value):
    emitted_case = get_emitted_case()

    test_helper.assertEqual(emitted_case['caseId'], context.emitted_uacs[0]['caseId'])
    test_helper.assertEqual(str(emitted_case[case_field]), expected_field_value)


@step("UAC_UPDATED messages are emitted with active set to true")
def check_uac_updated_msgs_emitted_with_qid_active(context):
    context.emitted_uacs = get_uac_updated_events(context.collex_id, len(context.emitted_cases))
    _check_uacs_updated_match_cases(context.emitted_uacs, context.emitted_cases_id)
    _check_new_uacs_are_active(context.emitted_uacs)


@step("{expected_count:d} UAC_UPDATED messages are emitted with active set to true")
def check_expected_number_of_uac_updated_msgs_emitted(context, expected_count):
    context.emitted_uacs = get_uac_updated_events(context.collex_id, expected_count)
    _check_new_uacs_are_active(context.emitted_uacs)

    included_case_ids = {event['caseId'] for event in context.emitted_uacs}

    # Overwrite the emitted cases and IDs so that they only contain the cases included in the print file
    context.emitted_cases = [case for case in context.emitted_cases if case['caseId'] in included_case_ids]
    context.emitted_cases_id = [emitted_case['caseId'] for emitted_case in context.emitted_cases]


def _check_new_uacs_are_active(emitted_uacs):
    for uac in emitted_uacs:
        test_helper.assertTrue(uac['active'], f'Newly created UAC QID pairs should be active,'
                                              f' QID: {uac["questionnaireId"]}')


def _check_uacs_updated_match_cases(uac_updated_events, case_ids):
    test_helper.assertSetEqual(set(uac['caseId'] for uac in uac_updated_events),
                               set(case_ids))

    test_helper.assertEqual(len(uac_updated_events), len(case_ids))
