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
    context.browser.find_by_id("sample_validation_rules_input").fill("[]")
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


@step('the "Add collection exercise" button is clicked')
def add_collection_exercise_button(context):
    context.browser.find_by_id("add-new-collection-exercise-button").click()


@step('a collection exercise called "{collecting_exercise_name}" plus unique suffix, with a start date of "{start_date}" and an end date of "{end_date}" is created')
def create_collection_exercise(context, collecting_exercise_name, start_date, end_date):
    context.collecting_exercise_name = collecting_exercise_name + get_random_alpha_numerics(5)
    context.collecting_exercise_start_date = dict(zip(["year", "month", "day"], start_date.split("-")))
    context.collecting_exercise_end_date = dict(zip(["year", "month", "day"], end_date.split("-")))
    context.browser.find_by_id("collection_exercise_name_input").fill(context.collecting_exercise_name)
    context.browser.find_by_id("description_input").fill(context.collecting_exercise_name)
    context.browser.find_by_id("start_date_input-day").fill(context.collecting_exercise_start_date["day"])
    context.browser.find_by_id("start_date_input-month").fill(context.collecting_exercise_start_date["month"])
    context.browser.find_by_id("start_date_input-year").fill(context.collecting_exercise_start_date["year"])
    context.browser.find_by_id("start_date_input-day").fill(end_date["day"])
    context.browser.find_by_id("start_date_input-month").fill(end_date["month"])
    context.browser.find_by_id("start_date_input-year").fill(end_date["year"])
    context.browser.find_by_id("collection_instrument_rules_input").fill('[{"foo": "bar"}]')
    context.browser.find_by_id("create-collection-exercise-button").click()


@step('I should see the new collection exercise details')
def find_collection_exercise_details(context):
    test_helper.assertEqual(
        context.browser.find_by_id("collection_exercise_name_value", wait_time=5).first.text,
        context.collecting_exercise_name,
        f"Expected collection exercise name to be {context.collecting_exercise_name},"
        f" but found {context.browser.find_by_id("collection_exercise_name_value").first.text}"
    )
    test_helper.assertIn(
        context.browser.find_by_id("start_date_value", wait_time=5).first.text,
        f"{context.collecting_exercise_start_date["year"]}-"
        f"{context.collecting_exercise_start_date["month"].zfill(2)}-"
        f"{context.collecting_exercise_start_date["day"].zfill(2)}",
    )
    test_helper.assertIn(
        context.browser.find_by_id("end_date_value", wait_time=5).first.text,
        f"{context.collecting_exercise_end_date["year"]}-"
        f"{context.collecting_exercise_end_date["month"].zfill(2)}-"
        f"{context.collecting_exercise_end_date["day"].zfill(2)}",
    )

@step("the {detail} name edit link is clicked")
def click_name_edit_link(context, detail):
    context.browser.find_by_id(f"{detail.join("_")}_name_edit_link", wait_time=5).first.click()


@step('the collection exercise name is changed to "{edited_name}"')
def change_survey_name(context, edited_name):
    context.edited_collection_exercise_name = edited_name + get_random_alpha_numerics(5)
    context.browser.find_by_id("collection_exercise_name_input").fill(context.edited_survey_name)
    context.browser.find_by_id("create-collection-exercise-button").click()


@step('I should see the edited collection name')
def find_edited_survey_name(context):
    test_helper.assertEqual(context.browser.find_by_id("collection_exercise_name_value", wait_time=5).first.text,
                            context.edited_collection_exercise_name,
                            f"Expected collection exercise name to be {context.edited_collection_exercise_name},"
                            f" but found {context.browser.find_by_id("collection_exercise_name_value").first.text}")
    test_helper.assertNotEqual(context.survey_name, context.edited_collection_exercise_name, "The collection exercise name was not edited")
