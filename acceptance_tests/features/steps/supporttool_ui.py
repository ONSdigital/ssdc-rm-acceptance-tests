import time
import json

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
