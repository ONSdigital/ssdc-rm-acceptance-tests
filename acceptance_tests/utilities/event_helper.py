from retrying import retry

from acceptance_tests.utilities.case_api_helper import get_logged_events_for_case_by_id
from acceptance_tests.utilities.test_case_helper import test_helper


@retry(stop_max_attempt_number=30, wait_fixed=1000)
def check_if_event_list_is_exact_match(event_type_list, case_id):
    actual_logged_events = get_logged_events_for_case_by_id(case_id)
    expected_logged_event_types = event_type_list.replace('[', '').replace(']', '').split(',')
    actual_logged_event_types = [event['eventType'] for event in actual_logged_events]

    test_helper.assertCountEqual(expected_logged_event_types, actual_logged_event_types,
                                 msg="Actual logged event types did not match expected")
