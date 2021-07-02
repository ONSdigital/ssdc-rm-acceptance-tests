import requests
from tenacity import retry, stop_after_delay, wait_fixed

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_logged_events_for_case_by_id(case_id):
    response = requests.get(f'{Config.CASE_API_CASE_URL}{case_id}?caseEvents=true')
    response.raise_for_status()
    response_json = response.json()
    return response_json['caseEvents']


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def check_if_event_list_is_exact_match(event_type_list, case_id):
    actual_logged_events = get_logged_events_for_case_by_id(case_id)
    expected_logged_event_types = event_type_list.replace('[', '').replace(']', '').split(',')
    actual_logged_event_types = [event['eventType'] for event in actual_logged_events]

    test_helper.assertCountEqual(expected_logged_event_types, actual_logged_event_types,
                                 msg="Actual logged event types did not match expected")
