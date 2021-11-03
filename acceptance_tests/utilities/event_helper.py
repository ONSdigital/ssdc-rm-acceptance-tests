from tenacity import retry, wait_fixed, stop_after_delay

from acceptance_tests.utilities.case_api_helper import get_logged_events_for_case_by_id
from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.pubsub_helper import get_exact_number_of_pubsub_messages
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_emitted_cases(expected_msg_count=1):
    messages_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                                            expected_msg_count=expected_msg_count,
                                                            timeout=60)

    case_payloads = []
    for message_received in messages_received:
        test_helper.assertEqual(message_received['header']['originatingUser'], Config.SAMPLE_LOAD_ORIGINATING_USER,
                                f'Unexpected originating user, all of messages_received: {messages_received}')
        case_payloads.append(message_received['payload']['caseUpdate'])

    return case_payloads


def get_emitted_case_update(correlation_id, originating_user):
    message_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION,
                                                           expected_msg_count=1)[0]

    if correlation_id:
        test_helper.assertEqual(message_received['header']['correlationId'], correlation_id,
                                'Unexpected correlation ID, does not match message received')

    if originating_user:
        test_helper.assertEqual(message_received['header']['originatingUser'], originating_user,
                                'Unexpected originating user')

    return message_received['payload']['caseUpdate']


def get_emitted_uac_update(correlation_id, originating_user):
    message_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                                           expected_msg_count=1)[0]

    if correlation_id:
        test_helper.assertEqual(message_received['header']['correlationId'], correlation_id,
                                'Unexpected correlation ID')

    if originating_user:
        test_helper.assertEqual(message_received['header']['originatingUser'], originating_user,
                                'Unexpected originating user')

    return message_received['payload']['uacUpdate']


def get_uac_update_events(expected_number, correlation_id, originating_user):
    messages_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION,
                                                            expected_msg_count=expected_number,
                                                            timeout=60)

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


def get_exactly_one_emitted_survey_update():
    message_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_SURVEY_SUBSCRIPTION,
                                                           expected_msg_count=1)[0]

    return message_received['payload']['surveyUpdate']


def get_emitted_collection_exercise_update():
    message_received = get_exact_number_of_pubsub_messages(Config.PUBSUB_OUTBOUND_COLLECTION_EXERCISE_SUBSCRIPTION,
                                                           expected_msg_count=1)[0]

    return message_received['payload']['collectionExerciseUpdate']


def get_emitted_case_events_by_type(case_id, type_filter):
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
                                f"The invalid case reason doesn't matched expected")
