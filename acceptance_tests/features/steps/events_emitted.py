from behave import step

from acceptance_tests.utilities.event_helper import check_invalid_case_reason_matches_on_event, \
    get_emitted_case_events_by_type, get_emitted_case_update, get_emitted_cases, get_emitted_uac_update, \
    get_uac_update_events, _check_uacs_updated_match_cases, _check_new_uacs_are_as_expected, \
    check_uac_update_msgs_emitted_with_qid_active_and_field_equals_value
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


@step('a CASE_UPDATE message is emitted where {new_values:json} are the updated values')
def case_update_msg_sent_with_multiple_values(context, new_values):
    emitted_case = get_emitted_case_update(context.correlation_id, context.originating_user)

    test_helper.assertEqual(emitted_case['caseId'], context.emitted_cases[0]['caseId'],
                            'The updated case is expected to be the first stored emitted case,'
                            f'emitted case: {emitted_case}')
    for key, value in new_values.items():
        test_helper.assertEqual(emitted_case[key], value,
                                f'The updated case field "{key}" equals "{emitted_case[key]}", must match '
                                f'the expected value "{value}". emitted case: {emitted_case}')


@step("UAC_UPDATE messages are emitted with active set to {active:boolean}")
def check_uac_update_msgs_emitted_with_qid_active(context, active):
    context.emitted_uacs = get_uac_update_events(len(context.emitted_cases), context.correlation_id,
                                                 context.originating_user)
    _check_uacs_updated_match_cases(context.emitted_uacs, context.emitted_cases)

    _check_new_uacs_are_as_expected(emitted_uacs=context.emitted_uacs, active=active,
                                    field_to_test='collectionInstrumentUrl',
                                    expected_value=context.expected_collection_instrument_url)


@step(
    'UAC_UPDATE message is emitted with active set to {active:boolean} and "{field_to_test}" is'
    ' {expected_value:boolean}')
def check_uac_update_msgs_emitted_with_qid_active_and_field_equals_value_step(context, active,
                                                                         field_to_test, expected_value):
    check_uac_update_msgs_emitted_with_qid_active_and_field_equals_value(context.emitted_cases, context.correlation_id,
                                                                         active, field_to_test, expected_value)


@step("{expected_count:d} UAC_UPDATE messages are emitted with active set to {active:boolean}")
def check_expected_number_of_uac_update_msgs_emitted(context, expected_count, active):
    context.emitted_uacs = get_uac_update_events(expected_count, context.correlation_id, context.originating_user)

    _check_new_uacs_are_as_expected(context.emitted_uacs, active)

    included_case_ids = {event['caseId'] for event in context.emitted_uacs}

    # Overwrite the emitted cases and IDs so that they only contain the cases included in the print file
    context.emitted_cases = [case for case in context.emitted_cases if case['caseId'] in included_case_ids]


@step("a CASE_UPDATED message is emitted for the case")
@step("a CASE_UPDATED message is emitted for the new case")
def check_case_updated_emitted_for_new_case(context):
    emitted_case = get_emitted_case_update(context.correlation_id, context.originating_user)
    test_helper.assertEqual(emitted_case['caseId'], context.case_id,
                            f'The emitted case, {emitted_case} does not match the case {context.case_id}')


@step("a CASE_UPDATE message is emitted for each bulk updated case with expected refusal type")
def case_emitted_with_field_set_to_value(context):
    emitted_updated_cases = get_emitted_cases(len(context.bulk_refusals))

    for emitted_case in emitted_updated_cases:
        test_helper.assertIn(emitted_case['caseId'], context.bulk_refusals.keys(),
                             f'Got case updated event {emitted_case}, '
                             f'not in expected bulk refusal caseIds {context.bulk_refusals.keys()}')

        expected_refusal_type = context.bulk_refusals[emitted_case['caseId']]

        test_helper.assertEqual(
            emitted_case['refusalReceived'],
            expected_refusal_type,
            'Refusal type on the case updated events should match the expected type from the bulk file,'
            f'received {emitted_case} expected type: {expected_refusal_type}')


@step("a CASE_UPDATE message is emitted for each bulk updated invalid case with correct reason")
def cases_emitted_for_bulk_invalid_with_correct_reason(context):
    emitted_updated_cases = get_emitted_cases(len(context.bulk_invalids))

    for emitted_case in emitted_updated_cases:
        test_helper.assertIn(emitted_case['caseId'], context.bulk_invalids.keys(),
                             f'Got case updated event {emitted_case}, '
                             f'not in expected bulk invalid caseIds {context.bulk_invalids.keys()}')

        expected_reason = context.bulk_invalids[emitted_case['caseId']]
        logged_invalid_events = get_emitted_case_events_by_type(emitted_case['caseId'], 'INVALID_CASE')
        test_helper.assertEqual(len(logged_invalid_events), 1,
                                msg=f'Expected 1 Invalid Case event, received {len(logged_invalid_events)}')

        check_invalid_case_reason_matches_on_event(logged_invalid_events[0]['id'], expected_reason)


@step("a CASE_UPDATE message is emitted for each bulk updated sample row")
def case_updated_messages_for_bulk_update_sample(context):
    emitted_updated_cases = get_emitted_cases(len(context.bulk_sample_update))

    for emitted_case in emitted_updated_cases:
        matching_expected_row = get_bulk_data_row_from_case_id_or_fail(context.bulk_sample_update,
                                                                       emitted_case['caseId'])
        expected_field_to_update = matching_expected_row["fieldToUpdate"]
        expected_value = matching_expected_row["newValue"]
        actual_value = emitted_case["sample"][expected_field_to_update]

        # Maybe overkill but check we're not merrily comparing 2 Nones
        test_helper.assertIsNotNone(actual_value,
                                    f"Missing actual new value in emitted_case['sample'] key"
                                    f" {expected_field_to_update}")
        test_helper.assertEqual(actual_value, expected_value, "Case Updated Sample doesn't match expected")


def get_bulk_data_row_from_case_id_or_fail(bulk_data, case_id):
    for data_row in bulk_data:
        if case_id == data_row["caseId"]:
            return data_row

    test_helper.fail(f"Case id {case_id} not found in {bulk_data}")


@step("a CASE_UPDATE message is emitted for each case with sensitive data redacted")
def case_update_message_emited_for_every_case_with_sensitive_data_redacted(context):
    emitted_updated_cases = get_emitted_cases(len(context.bulk_sensitive_update))

    for emitted_case in emitted_updated_cases:
        bulk_update_for_case = get_bulk_data_row_from_case_id_or_fail(context.bulk_sensitive_update,
                                                                      emitted_case['caseId'])
        test_helper.assertEqual(emitted_case["sampleSensitive"][bulk_update_for_case['fieldToUpdate']], "REDACTED",
                                f"Expected emitted_case['sampleSensitive'][{bulk_update_for_case['fieldToUpdate']}] "
                                "to equal 'REDACTED'")


@step("a CASE_UPDATED message is emitted for the case with correct sensitive data")
def case_updated_emitted_with_correct_sensitve_data(context):
    emitted_case = get_emitted_case_update(context.correlation_id, context.originating_user)
    test_helper.assertEqual(emitted_case['caseId'], context.case_id,
                            f'The emitted case, {emitted_case} does not match the case {context.case_id}')
    test_helper.assertEqual(emitted_case["sampleSensitive"]['PHONE_NUMBER'], "REDACTED",
                            "Expected emitted_case['sampleSensitive']['PHONE_NUMBER'] to equal 'REDACTED'")
