import requests

from behave import step

from acceptance_tests.utilities.event_helper import check_if_event_list_is_exact_match
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step('there is a request for telephone capture of a case')
def request_telephone_capture(context):
    response = requests.get(f'{Config.CASE_API_CASE_URL}{context.loaded_case_ids[0]}/telephone-capture')
    response.raise_for_status()
    context.telephone_capture_request = response.json()


@step('a UAC and QID with questionnaire type "{qid_type}" type are generated and returned')
def check_telephone_capture_generated(context, qid_type):
    test_helper.assertIsNotNone(context.telephone_capture_request.get('uac'))
    test_helper.assertEqual(context.telephone_capture_request['qid'][:2], qid_type)


@step("the events logged for the case requesting telephone capture are {expected_event_list}")
def check_survey_launch_event_logging(context, expected_event_list):
    check_if_event_list_is_exact_match(expected_event_list, context.loaded_case_ids[0])
