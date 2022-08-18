import time
import json
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import get_random_alpha_numerics
from acceptance_tests.utilities.test_case_helper import test_helper
from acceptance_tests.utilities.validation_rule_helper import get_sample_rows_and_generate_open_validation_rules
from config import Config

SAMPLE_FILES_PATH = Config.RESOURCE_FILE_PATH.joinpath('sample_files')


@step("the support tool landing page is displayed")
def support_tool_landing_page_navigated_to(context):
    context.browser.visit(f'{Config.SUPPORT_TOOL_URL}')


@step("The Create Survey Button is clicked on")
def click_on_create_survey_button(context):
    context.browser.find_by_id('createSurveyBtn').click()


@step(
    'a Survey called "{survey_prefix}" plus unique suffix is created for sample file "{sample_file_name}"')
def create_survey_in_UI(context, survey_prefix, sample_file_name):
    context.survey_name = survey_prefix + get_random_alpha_numerics(5)
    context.browser.find_by_id('surveyNameTextField').fill(context.survey_name)

    Config.RESOURCE_FILE_PATH.joinpath('sample_files')
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_generate_open_validation_rules(sample_file_path)

    context.browser.find_by_id('validationRulesTextField').fill(json.dumps(sample_validation_rules))

    context.browser.find_by_id('surveyDefinitionURLTextField').fill("http://foo.bar.json")
    context.browser.find_by_id('postCreateSurveyBtn').click()

    test_helper.assertEquals(
        len(context.browser.find_by_id('surveyListTable').first.find_by_text(context.survey_name)), 1)


@step('the survey is clicked on it should display the collex page')
def click_into_collex_page(context):
    context.browser.find_by_id('surveyListTable').first.find_by_text(context.survey_name).click()


@step('the create collection exercise button is clicked on and entered in details')
def click_create_collex_button(context):
    context.browser.find_by_id('createCollectionExerciseBtn').click()
    context.collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    context.browser.find_by_id('collectionExerciseNameTextField').fill(context.collex_name)

    context.expected_collection_instrument_url = "http://test-eq.com/test-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 100,
            "spelExpression": "caze.sample['POSTCODE'] == 'NW16 FNK'",
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        },
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": "this URL should not be chosen. If it is, the test is a failure"
        }
    ]
    context.browser.find_by_id('collectionExerciseReferenceTextField').fill('MVP012021')
    context.browser.find_by_id('collectionExerciseCIRulesTextField').fill(json.dumps(collection_instrument_selection_rules))
    context.browser.find_by_id('postCreateCollectionExerciseBtn').click()
    test_helper.assertEquals(
        len(context.browser.find_by_id('collectionExerciseTableList').first.find_by_text(context.collex_name)), 1)

@step('the collex is clicked on and displays the details page')
def click_into_collex_details(context):
    context.browser.find_by_id('collectionExerciseTableList').first.find_by_text(context.collex_name).click()


@step('I click the upload sample file button with file "{sample_file_name}"')
def click_load_sample(context, sample_file_name):
    Config.RESOURCE_FILE_PATH.joinpath('sample_files')
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    context.browser.find_by_id('contained-button-file').first.type(str(sample_file_path))
    context.browser.reload()
    test_helper.assertEquals(
        len(context.browser.find_by_id('sampleFilesList').first.find_by_text(sample_file_name)), 1)
    print(context.browser.find_by_id('sampleFilesList').first.find_by_text(sample_file_name))



