from behave import step

from acceptance_tests.utilities.audit_trail_helper import get_random_alpha_numerics
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("the support frontend is displayed")
def navigating_to_the_support_frontend_landing_page(context):
    context.browser.visit(f"{Config.SUPPORT_FRONTEND_URL}/surveys")


@step('the "Create new survey" button is clicked')
def click_on_create_new_survey_button(context):
    context.browser.find_by_id("create-new-survey-button").click()


@step('a survey called "{survey_name}" plus unique suffix is created')
def input_survey_details_and_save_survey(context, survey_name):
    context.survey_name = survey_name + get_random_alpha_numerics(5)
    context.browser.find_by_id("name_input").fill(context.survey_name)
    context.browser.find_by_id("sample_definition_url_input").fill(survey_name)
    context.browser.find_by_id("sample_validation_rules_input").fill("{}")
    context.browser.find_by_id("create-survey-button").click()


@step("I should see the new surveys details")
def find_survey_details(context):
    test_helper.assertEqual(
        context.browser.find_by_id("name_value", wait_time=5).first.text,
        context.survey_name,
        f"Expected survey name to be {context.survey_name},"
        f" but found {context.browser.find_by_id("name_value").first.text}"
    )


@step("the name edit link is clicked")
def click_name_edit_link(context):
    context.browser.find_by_id("name_edit_link", wait_time=5).first.click()


@step('the name is changed to "{edited_name}"')
def change_survey_name(context, edited_name):
    context.edited_survey_name = edited_name + get_random_alpha_numerics(5)
    context.browser.find_by_id("name_input").fill(context.edited_survey_name)
    context.browser.find_by_id("create-survey-button").click()


@step('I should see the edited survey name')
def find_edited_survey_name(context):
    test_helper.assertEqual(context.browser.find_by_id("name_value", wait_time=5).first.text,
                            context.edited_survey_name,
                            f"Expected survey name to be {context.edited_survey_name},"
                            f" but found {context.browser.find_by_id("name_value").first.text}")
    test_helper.assertNotEqual(context.survey_name, context.edited_survey_name, "The survey name was not edited")
