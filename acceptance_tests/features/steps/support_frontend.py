from behave import step

from acceptance_tests.utilities.audit_trail_helper import get_random_alpha_numerics
from acceptance_tests.utilities.event_helper import get_collection_exercise_update_by_name
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


@step('a survey with no filed entered is attempted to be created')
def create_survey_with_no_name(context):
    context.browser.find_by_id("create-survey-button").click()


@step('I should see {num_errors} problems with this page')
def see_number_of_problems(context, num_errors):
    test_helper.assertEqual(context.browser.find_by_id("alert", wait_time=5).first.text,
                            f"There are {num_errors} problems with this page", "No error summary shown")


@step('I see a "{text}" error')
def see_a_text_error(context, text):
    test_helper.assertTrue(context.browser.is_text_present(text), f"No error {text} message shown")


@step('fields are emptied')
def empty_fields(context):
    context.browser.find_by_id("name_input", wait_time=5).fill("")
    context.browser.find_by_id("sample_definition_url_input").fill("")
    radios = context.browser.find_by_css("input[type='radio']:checked")
    if radios:
        radios[0].click()
    context.browser.find_by_id("create-survey-button").click()


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


@step('the "Add collection exercise" button is clicked')
def add_collection_exercise_button(context):
    context.browser.find_by_id("add-new-collection-exercise-button").click()


@step(
    'a collection exercise called "{collection_exercise_name}" plus unique suffix,'
    ' with a start date of "{start_date}" and an end date of "{end_date}" is created'
)
def create_collection_exercise(context, collection_exercise_name, start_date, end_date):
    context.collection_exercise_name = collection_exercise_name + get_random_alpha_numerics(5)
    context.collection_exercise_start_date = dict(zip(["year", "month", "day"], start_date.split("-")))
    context.collection_exercise_end_date = dict(zip(["year", "month", "day"], end_date.split("-")))
    context.browser.find_by_id("collection_exercise_name_input").fill(context.collection_exercise_name)
    context.browser.find_by_id("description_input").fill(context.collection_exercise_name)
    context.browser.find_by_id("start_date_input-day").fill(context.collection_exercise_start_date["day"])
    context.browser.find_by_id("start_date_input-month").fill(context.collection_exercise_start_date["month"])
    context.browser.find_by_id("start_date_input-year").fill(context.collection_exercise_start_date["year"])
    context.browser.find_by_id("end_date_input-day").fill(context.collection_exercise_end_date["day"])
    context.browser.find_by_id("end_date_input-month").fill(context.collection_exercise_end_date["month"])
    context.browser.find_by_id("end_date_input-year").fill(context.collection_exercise_end_date["year"])
    context.browser.find_by_id("collection_instrument_rules_input").fill('[{"foo": "bar"}]')
    context.browser.find_by_id("create-collection-exercise-button").click()


@step('I should see the new collection exercise details')
def find_collection_exercise_details(context):
    test_helper.assertEqual(
        context.browser.find_by_id("collection_exercise_name_value", wait_time=5).first.text,
        context.collection_exercise_name,
        f"Expected collection exercise name to be {context.collection_exercise_name},"
        f" but found {context.browser.find_by_id("collection_exercise_name_value").first.text}"
    )
    test_helper.assertIn(
        f"{context.collection_exercise_start_date["year"]}-"
        f"{context.collection_exercise_start_date["month"].zfill(2)}-"
        f"{context.collection_exercise_start_date["day"].zfill(2)}",
        context.browser.find_by_id("start_date_value", wait_time=5).first.text
    )
    test_helper.assertIn(
        f"{context.collection_exercise_end_date["year"]}-"
        f"{context.collection_exercise_end_date["month"].zfill(2)}-"
        f"{context.collection_exercise_end_date["day"].zfill(2)}",
        context.browser.find_by_id("end_date_value", wait_time=5).first.text
    )


@step('the {collex_type} collection exercise is emitted')
def check_collection_exercise_is_emitted(context, collex_type):
    collection_exercise_name = ""
    if collex_type == "new":
        collection_exercise_name = context.collection_exercise_name
    elif collex_type == "edited":
        collection_exercise_name = context.edited_collection_exercise_name
    get_collection_exercise_update_by_name(collection_exercise_name, context.test_start_utc_datetime)


@step("the collection exercise name edit link is clicked")
def click_collection_exercise_name_edit_link(context):
    context.browser.find_by_id("collection_exercise_name_edit_link", wait_time=5).first.click()


@step('the collection exercise name is changed to "{edited_name}"')
def change_collection_exercise_name(context, edited_name):
    context.edited_collection_exercise_name = edited_name + get_random_alpha_numerics(5)
    context.browser.find_by_id("collection_exercise_name_input").fill(context.edited_collection_exercise_name)
    context.browser.find_by_id("create-collection-exercise-button").click()


@step('I should see the edited collection name')
def find_edited_collection_exercise_name(context):
    test_helper.assertEqual(context.browser.find_by_id("collection_exercise_name_value", wait_time=5).first.text,
                            context.edited_collection_exercise_name,
                            f"Expected collection exercise name to be {context.edited_collection_exercise_name},"
                            f" but found {context.browser.find_by_id("collection_exercise_name_value").first.text}")
    test_helper.assertNotEqual(context.collection_exercise_name,
                               context.edited_collection_exercise_name,
                               "The collection exercise name was not edited")
