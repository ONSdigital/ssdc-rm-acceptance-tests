from behave import step

from acceptance_tests.utilities.case_api_helper import check_if_event_list_is_exact_match


@step("the events logged against the case are {expected_event_list}")
def check_case_events_logged(context, expected_event_list):
    check_if_event_list_is_exact_match(expected_event_list, context.emitted_cases_id[0])
