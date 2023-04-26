from functools import partial

from tenacity import retry, wait_fixed, stop_after_delay

from acceptance_tests.utilities.case_api_helper import get_logged_events_for_case_by_id
from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.pubsub_helper import get_exact_number_of_pubsub_messages, \
    get_matching_pubsub_message_acking_others
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_emitted_cases(expected_msg_count=1, test_start_time=None):
    messages_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                                            expected_msg_count=expected_msg_count,
                                                            test_start_time=test_start_time)

    case_payloads = []
    for message_received in messages_received:
        test_helper.assertEqual(message_received['header']['originatingUser'], Config.SAMPLE_LOAD_ORIGINATING_USER,
                                f'Unexpected originating user, all of messages_received: {messages_received}')
        case_payloads.append(message_received['payload']['caseUpdate'])

    return case_payloads


def get_emitted_case_update(correlation_id, originating_user, test_start_time):
    message_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                                           expected_msg_count=1, test_start_time=test_start_time)[0]

    if correlation_id:
        test_helper.assertEqual(message_received['header']['correlationId'], correlation_id,
                                'Unexpected correlation ID, does not match message received')

    if originating_user:
        test_helper.assertEqual(message_received['header']['originatingUser'], originating_user,
                                'Unexpected originating user')

    return message_received['payload']['caseUpdate']


def get_emitted_uac_update(correlation_id, originating_user, test_start_time):
    message_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                                           expected_msg_count=1, test_start_time=test_start_time)[0]

    if correlation_id:
        test_helper.assertEqual(message_received['header']['correlationId'], correlation_id,
                                'Unexpected correlation ID')

    if originating_user:
        test_helper.assertEqual(message_received['header']['originatingUser'], originating_user,
                                'Unexpected originating user')

    return message_received['payload']['uacUpdate']


def get_uac_update_events(expected_number, correlation_id, originating_user, test_start_time):
    messages_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                                            expected_msg_count=expected_number,
                                                            test_start_time=test_start_time)

    uac_payloads = []
    for uac_event in messages_received:
        if correlation_id:
            test_helper.assertEqual(uac_event['header']['correlationId'], correlation_id,
                                    f'Unexpected correlation ID, full messages received {messages_received}')

        if originating_user:
            test_helper.assertEqual(uac_event['header']['originatingUser'], originating_user,
                                    f'Unexpected originating user,  full messages received {messages_received}')

        uac_payloads.append(uac_event['payload']['uacUpdate'])

    return uac_payloads


def get_exactly_one_emitted_survey_update(test_start_time):
    message_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_SURVEY_SUBSCRIPTION,
                                                           expected_msg_count=1,
                                                           test_start_time=test_start_time)[0]

    return message_received['payload']['surveyUpdate']


def get_collection_exercise_update_by_name(collex_name, test_start_time):
    def collex_name_matcher(message, expected_collex_name=None):
        message_collex_name = message['payload']['collectionExerciseUpdate']['name']
        return (True, None) if message_collex_name == expected_collex_name else \
            (False, f'Collection exercise name "{message_collex_name}" did not match expected "{expected_collex_name}"')

    message_received = get_matching_pubsub_message_acking_others(
        Config.PUBSUB_OUTBOUND_COLLECTION_EXERCISE_SUBSCRIPTION,
        partial(collex_name_matcher, expected_collex_name=collex_name),
        test_start_time)

    return message_received['payload']['collectionExerciseUpdate']


def get_logged_case_events_by_type(case_id, type_filter):
    events = get_logged_events_for_case_by_id(case_id)

    logged_event_of_type = []

    for event in events:
        if event['eventType'] == type_filter:
            logged_event_of_type.append(event)

    return logged_event_of_type


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def check_invalid_case_reason_matches_on_event(event_id, expected_reason):
    with open_cursor() as cur:
        cur.execute("SELECT payload FROM casev3.event WHERE id = %s", (event_id,))
        result = cur.fetchone()

        test_helper.assertEqual(result[0]['invalidCase']['reason'], expected_reason,
                                "The invalid case reason doesn't matched expected")


def check_uac_update_msgs_emitted_with_qid_active_and_field_equals_value(emitted_cases, correlation_id, active,
                                                                         field_to_test, expected_value,
                                                                         test_start_time):
    emitted_uacs = get_uac_update_events(len(emitted_cases), correlation_id, None, test_start_time=test_start_time)
    _check_uacs_updated_match_cases(emitted_uacs, emitted_cases)
    _check_new_uacs_are_as_expected(emitted_uacs, active, field_to_test, expected_value)

    return emitted_uacs


def _check_uacs_updated_match_cases(uac_update_events, cases):
    test_helper.assertSetEqual(set(uac['caseId'] for uac in uac_update_events),
                               set(case['caseId'] for case in cases),
                               'The UAC updated events should be linked to the given set of case IDs')

    test_helper.assertEqual(len(uac_update_events), len(cases),
                            'There should be one and only one UAC updated event for each given case ID,'
                            f'uac_update_events: {uac_update_events} '
                            f'cases {cases}')


def _check_new_uacs_are_as_expected(emitted_uacs, active, field_to_test=None, expected_value=None):
    for uac in emitted_uacs:
        test_helper.assertEqual(uac['active'], active, f"UAC {uac} active status doesn't equal expected {active}")

        if field_to_test:
            test_helper.assertEqual(uac[field_to_test], expected_value,
                                    f"UAC {uac} field {field_to_test} doesn't equal expected {expected_value}")
