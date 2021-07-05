from behave import step

from acceptance_tests.utilities.event_helper import get_emitted_case_update, get_emitted_uac_update, \
    get_uac_updated_events
from acceptance_tests.utilities.test_case_helper import test_helper


@step("a UAC_UPDATED message is emitted with active set to false")
def uac_updated_msg_emitted(context):
    emitted_uac = get_emitted_uac_update()
    test_helper.assertEqual(emitted_uac['caseId'], context.emitted_cases[0]['caseId'],
                            'The UAC_UPDATED message case ID must match the first case ID')
    test_helper.assertFalse(emitted_uac['active'], 'The UAC_UPDATED message should active flag "false"')


@step('a CASE_UPDATED message is emitted where "{case_field}" is "{expected_field_value}"')
def case_updated_msg_sent_with_values(context, case_field, expected_field_value):
    emitted_case = get_emitted_case_update()

    test_helper.assertEqual(emitted_case['caseId'], context.emitted_cases[0]['caseId'],
                            'The updated case is expected to be the first stored emitted case')
    test_helper.assertEqual(str(emitted_case[case_field]), expected_field_value,
                            'The updated case field must match the expected value')


@step("UAC_UPDATED messages are emitted with active set to {active_str}")
def check_uac_updated_msgs_emitted_with_qid_active(context, active_str):
    context.emitted_uacs = get_uac_updated_events(len(context.emitted_cases))
    _check_uacs_updated_match_cases(context.emitted_uacs, context.emitted_cases)

    active = False
    if active_str == 'true':
        active = True
    _check_new_uacs_are_as_expected(context.emitted_uacs, context.collex_id, active)


@step("{expected_count:d} UAC_UPDATED messages are emitted with active set to {active_str}")
def check_expected_number_of_uac_updated_msgs_emitted(context, expected_count, active_str):
    context.emitted_uacs = get_uac_updated_events(expected_count)

    active = False
    if active_str == 'true':
        active = True
    _check_new_uacs_are_as_expected(context.emitted_uacs, context.collex_id, active)

    included_case_ids = {event['caseId'] for event in context.emitted_uacs}

    # Overwrite the emitted cases and IDs so that they only contain the cases included in the print file
    context.emitted_cases = [case for case in context.emitted_cases if case['caseId'] in included_case_ids]


def _check_new_uacs_are_as_expected(emitted_uacs, collex_id, active):
    for uac in emitted_uacs:
        test_helper.assertEqual(uac['active'], active)
        test_helper.assertEqual(uac['collectionExerciseId'], str(collex_id),
                                f'UAC updates should all be for the current collection exericse,'
                                f' QID: {uac["questionnaireId"]}')
        test_helper.assertTrue(uac['active'],
                               f'Newly created UAC QID pairs should be active, QID: {uac["questionnaireId"]}')
        test_helper.assertIsNotNone(uac['caseId'], f'Newly created UAC QID pairs should always be linked to a case, '
                                                   f'QID without link: {uac["questionnaireId"]}')


def _check_uacs_updated_match_cases(uac_updated_events, cases):
    test_helper.assertSetEqual(set(uac['caseId'] for uac in uac_updated_events),
                               set(case['caseId'] for case in cases),
                               'The UAC updated events should be linked to the given set of case IDs')

    test_helper.assertEqual(len(uac_updated_events), len(cases),
                            'There should be one and only one UAC updated event for each given case ID')
