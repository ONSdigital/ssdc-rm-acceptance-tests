from behave import step

from acceptance_tests.utilities.event_helper import get_emitted_case_update, get_emitted_uac_update, \
    get_uac_update_events
from acceptance_tests.utilities.test_case_helper import test_helper


@step("a UAC_UPDATE message is emitted with active set to false")
def uac_update_msg_emitted(context):
    emitted_uac = get_emitted_uac_update(context.correlation_id, context.originating_user)
    test_helper.assertEqual(emitted_uac['caseId'], context.emitted_cases[0]['caseId'],
                            f'The UAC_UPDATE message case ID must match the first case ID, emitted_uac {emitted_uac}')
    test_helper.assertFalse(emitted_uac['active'], 'The UAC_UPDATE message should active flag "false", '
                                                   f'emitted_uac {emitted_uac}')


@step('a CASE_UPDATE message is emitted where "{case_field}" is "{expected_field_value}"')
def case_update_msg_sent_with_values(context, case_field, expected_field_value):
    emitted_case = get_emitted_case_update(context.correlation_id, context.originating_user)

    test_helper.assertEqual(emitted_case['caseId'], context.emitted_cases[0]['caseId'],
                            'The updated case is expected to be the first stored emitted case,'
                            f'emitted case: {emitted_case}')
    test_helper.assertEqual(str(emitted_case[case_field]), expected_field_value,
                            f'The updated case field must match the expected value, emitted case: {emitted_case}')


@step("UAC_UPDATE messages are emitted with active set to {active:boolean}")
def check_uac_update_msgs_emitted_with_qid_active(context, active):
    context.emitted_uacs = get_uac_update_events(len(context.emitted_cases), context.correlation_id,
                                                 context.originating_user)
    _check_uacs_updated_match_cases(context.emitted_uacs, context.emitted_cases)

    _check_new_uacs_are_as_expected(context.emitted_uacs, active)


@step("{expected_count:d} UAC_UPDATE messages are emitted with active set to {active:boolean}")
def check_expected_number_of_uac_update_msgs_emitted(context, expected_count, active):
    context.emitted_uacs = get_uac_update_events(expected_count, context.correlation_id, context.originating_user)

    _check_new_uacs_are_as_expected(context.emitted_uacs, active)

    included_case_ids = {event['caseId'] for event in context.emitted_uacs}

    # Overwrite the emitted cases and IDs so that they only contain the cases included in the print file
    context.emitted_cases = [case for case in context.emitted_cases if case['caseId'] in included_case_ids]


def _check_new_uacs_are_as_expected(emitted_uacs, active):
    for uac in emitted_uacs:
        test_helper.assertEqual(uac['active'], active)


def _check_uacs_updated_match_cases(uac_update_events, cases):
    test_helper.assertSetEqual(set(uac['caseId'] for uac in uac_update_events),
                               set(case['caseId'] for case in cases),
                               'The UAC updated events should be linked to the given set of case IDs')

    test_helper.assertEqual(len(uac_update_events), len(cases),
                            'There should be one and only one UAC updated event for each given case ID,'
                            f'uac_update_events: {uac_update_events} '
                            f'cases {cases}')
