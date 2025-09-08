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
    context.browser.find_by_id("name_input", wait_time=5).fill(context.survey_name)
    context.browser.find_by_id("sample_definition_url_input").fill(survey_name)
    radios = context.browser.find_by_css("input[type='radio']")
    radios[0].click()
    button = context.browser.find_by_id("create-survey-button")
    context.browser.execute_script("arguments[0].scrollIntoView(true);", button._element)
    button.click()


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


@step('a survey with no filed entered is attempted to be created')
def create_survey_with_no_name(context):
    context.browser.find_by_id("create-survey-button").click()


@step('I should see error messages')
def see_error_messages(context):
    test_helper.assertEqual(context.browser.find_by_id("alert", wait_time=5).first.text,
                            "There are 3 problems with this page", "No error summary shown")
    test_helper.assertTrue(context.browser.is_text_present("Enter a survey name"), "No error message shown for name")
    test_helper.assertTrue(context.browser.is_text_present("Enter a sample definition URL"),
                           "No error message shown for sample definition URL")
    test_helper.assertTrue(context.browser.is_text_present("Select a sample template"),
                           "No error message shown for sample template")


@step('fields are emptied')
def empty_fields(context):
    context.browser.find_by_id("name_input", wait_time=5).fill("")
    context.browser.find_by_id("sample_definition_url_input").fill("")
    radios = context.browser.find_by_css("input[type='radio']:checked")
    if radios:
        radios[0].click()
    context.browser.find_by_id("create-survey-button").click()


@step('I should see error messages other than for sample template')
def see_error_messages_minus_template(context):
    test_helper.assertEqual(context.browser.find_by_id("alert", wait_time=5).first.text,
                            "There are 2 problems with this page", "No error summary shown")
    test_helper.assertTrue(context.browser.is_text_present("Enter a survey name"),
                           "No error message shown for name")
    test_helper.assertTrue(context.browser.is_text_present("Enter a sample definition URL"),
                           "No error message shown for sample definition URL")


@step('a survey with a name longer than 255 characters is attempted to be created')
def create_survey_with_long_name(context):
    long_name = "This is a very long survey name that is definitely going to be longer than 255 characters. " \
                "In fact, it is so long that it just keeps going and going and going and going and going and going " \
                "and going and going and going and going and going and going and going and going and going and " \
                "going and going and going and going and going and going and going and going and going and going " \
                "and going and going and going and going and going and going and going!"
    context.browser.find_by_id("name_input", wait_time=5).fill(long_name)
    context.browser.find_by_id("sample_definition_url_input").fill("Test URL")
    radios = context.browser.find_by_css("input[type='radio']")
    radios[0].click()


@step('the name should be truncated to 255 characters')
def name_truncated_to_255_characters(context):
    test_helper.assertEqual(len(context.browser.find_by_id("name_input").first.value), 255,
                            "The survey name is not 255 characters long")
