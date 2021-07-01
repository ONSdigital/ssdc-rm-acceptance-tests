from behave import step

from acceptance_tests.utilities.event_helper import check_if_event_list_is_exact_match


@step("the events logged for the case the respondent has authenticated against are {expected_event_list}")
@step("the events logged for the case requesting telephone capture are {expected_event_list}")
@step("the events logged for the refused case are {expected_event_list}")
@step("the events logged for the receipted case are {expected_event_list}")
@step("the events logged for the case with an invalid address are {expected_event_list}")
@step("the events logged for the survey launched case are {expected_event_list}")
def check_case_events_logged(context, expected_event_list):
    check_if_event_list_is_exact_match(expected_event_list, context.loaded_case_ids[0])
