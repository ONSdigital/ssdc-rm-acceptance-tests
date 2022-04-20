from typing import List

from behave import step

from acceptance_tests.utilities.case_api_helper import check_if_event_list_is_exact_match


@step("the events logged against the case are {expected_event_list:array}")
def check_case_events_logged(context, expected_event_list: List):
    check_if_event_list_is_exact_match(expected_event_list, context.emitted_cases[0]['caseId'])
