import json
import uuid
from datetime import datetime
from typing import List

from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tenacity import retry, stop_after_delay, wait_fixed

from acceptance_tests.features.steps.email_action_rule import check_notify_called_with_correct_emails_and_uacs
from acceptance_tests.features.steps.export_file import check_export_file
from acceptance_tests.utilities.audit_trail_helper import get_random_alpha_numerics
from acceptance_tests.utilities.event_helper import get_emitted_cases, \
    get_collection_exercise_update_by_name, \
    get_number_of_uac_update_events
from acceptance_tests.utilities.sample_helper import read_sample
from acceptance_tests.utilities.survey_helper import get_emitted_survey_update
from acceptance_tests.utilities.test_case_helper import test_helper
from acceptance_tests.utilities.validation_rule_helper import get_sample_rows_and_generate_open_validation_rules
from config import Config


@step("the support tool landing page is displayed")
def navigate_to_support_tool_landing_page(context):
    context.browser.visit(f'{Config.SUPPORT_TOOL_UI_URL}')


@step("the Create Survey Button is clicked on")
def click_on_create_survey_button(context):
    context.browser.find_by_id('createSurveyBtn').click()


@step(
    'a Survey called "{survey_prefix}" plus unique suffix is created for sample file "{sample_file_name}" '
    'with sensitive columns {sensitive_columns:array}')
def create_survey_in_ui(context, survey_prefix, sample_file_name, sensitive_columns):
    context.survey_name = survey_prefix + get_random_alpha_numerics(5)
    context.browser.find_by_id('surveyNameTextField').fill(context.survey_name)

    sample_file_path = Config.SAMPLE_FILES_PATH.joinpath(sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_generate_open_validation_rules(sample_file_path,
                                                                                              sensitive_columns)
    context.sample = read_sample(sample_file_path, sample_validation_rules)

    context.browser.find_by_id('validationRulesTextField').fill(json.dumps(sample_validation_rules))

    context.browser.find_by_id('surveyDefinitionURLTextField').fill("http://foo.bar.json")
    context.browser.find_by_id('postCreateSurveyBtn').click()

    test_helper.assertEqual(
        len(context.browser.find_by_id('surveyListTable').first.find_by_text(context.survey_name, wait_time=30)), 1)

    get_emitted_survey_update(context.survey_name, context.test_start_utc_datetime)


@step('the survey is clicked on it should display the collection exercise page')
def click_into_collex_page(context):
    context.browser.find_by_id('surveyListTable').first.find_by_text(context.survey_name).click()


@step('the create collection exercise button is clicked, the details are submitted and the exercise is created')
def click_create_collex_button(context):
    context.browser.find_by_id('createCollectionExerciseBtn', wait_time=30).click()
    context.collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    context.browser.find_by_id('collectionExerciseNameTextField').fill(context.collex_name)

    context.expected_collection_instrument_url = "http://test-eq.com/test-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 100,
            "spelExpression": "caze.sample['schoolId'] == '123'",
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        },
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": "this URL should not be chosen. If it is, the test is a failure"
        }
    ]
    context.browser.find_by_id('collectionExerciseReferenceTextField').fill('MVP012021')
    context.browser.find_by_id('collectionExerciseCIRulesTextField').fill(
        json.dumps(collection_instrument_selection_rules))
    context.browser.find_by_id('postCreateCollectionExerciseBtn').click()
    test_helper.assertEqual(
        len(context.browser.find_by_id('collectionExerciseTableList').first.find_by_text(context.collex_name)), 1)

    get_collection_exercise_update_by_name(context.collex_name, context.test_start_utc_datetime)


@step('the collection exercise is clicked on, navigating to the selected exercise details page')
def click_into_collex_details(context):
    context.browser.find_by_id('collectionExerciseTableList').first.find_by_text(context.collex_name,
                                                                                 wait_time=30).click()


@step('I click the upload sample file button with file "{sample_file_name}"')
def click_load_sample(context, sample_file_name):
    sample_file_path = Config.SAMPLE_FILES_PATH.joinpath(sample_file_name)
    context.browser.find_by_id('contained-button-file').first.type(str(sample_file_path))
    context.sample_count = sum(1 for _ in open(sample_file_path)) - 1
    test_helper.assertEqual(
        len(context.browser.find_by_id('sampleFilesList').first.find_by_text(sample_file_name, wait_time=30)), 1)
    context.browser.find_by_id('sampleFilesList').first.find_by_id("sampleStatus0").click()
    context.browser.find_by_id("jobProcessBtn", wait_time=30).click()
    poll_sample_status_processed(context.browser)
    context.browser.find_by_id('closeSampledetailsBtn').click()
    context.emitted_cases = get_emitted_cases(context.sample_count, context.test_start_utc_datetime,
                                              originating_user_email=Config.UI_USER_EMAIL)

    test_helper.assertEqual(len(context.emitted_cases), context.sample_count)


@retry(wait=wait_fixed(2), stop=stop_after_delay(30))
def poll_sample_status_processed(browser):
    test_helper.assertEqual(browser.find_by_id('sampleFilesList').first.find_by_id("sampleStatus0").text, "PROCESSED")


@step('the Create Export File Template button is clicked on')
def click_create_export_file_template_button(context):
    context.browser.find_by_id('createExportFileTemplateBtn').click()


@step('an export file template with packcode "{packcode}" and template {template:array} has been created')
def create_export_file_template(context, packcode, template: List):
    context.pack_code = f'{packcode}-' + get_random_alpha_numerics(5)
    context.template = template
    context.browser.find_by_id('packCodeTextField').fill(context.pack_code)
    context.browser.find_by_id('descriptionTextField').fill('export-file description')
    context.browser.find_by_id('exportFileDestinationSelectField').click()
    context.browser.find_by_id(Config.SUPPLIER_DEFAULT_TEST).click()
    context.browser.find_by_id('templateTextField').fill(str(context.template).replace('\'', '\"'))
    context.browser.find_by_id('createExportFileTemplateInnerBtn').click()


@step('I should see the export file template in the template list')
def find_created_export_file(context):
    test_helper.assertEqual(
        len(context.browser.find_by_id('exportFileTemplateTable', wait_time=30).first
            .find_by_text(context.pack_code, wait_time=30)), 1)


@step("the export file template has been added to the allow on action rule list")
def allow_export_file_template_on_action_rule(context):
    context.browser.find_by_id('actionRuleExportFileTemplateBtn').click()
    context.browser.find_by_id('allowExportFileTemplateSelect').click()
    context.browser.find_by_value(context.pack_code, wait_time=30).click()
    context.browser.find_by_id("addAllowExportFileTemplateBtn").click()


@step("I create an action rule")
def click_action_rule_button(context):
    context.browser.find_by_id('createActionRuleDialogBtn').click()
    context.browser.find_by_id('selectActionRuleType').click()
    context.browser.find_by_value('Export File').click()
    context.browser.find_by_id('selectActionRuleExportFilePackCode').click()
    context.browser.find_by_id(context.pack_code, wait_time=30).click()
    context.browser.find_by_id('createActionRuleBtn').click()


@step('I can see the Action Rule has been triggered and export files have been created')
def check_for_action_rule_completed(context):
    poll_action_rule_completed(context.browser, context.pack_code)
    context.emitted_uacs = get_number_of_uac_update_events(context.sample_count, context.test_start_utc_datetime)
    check_export_file(context)


@retry(wait=wait_fixed(2), stop=stop_after_delay(120))
def poll_action_rule_completed(browser, pack_code):
    browser.reload()
    test_helper.assertEqual(
        len(browser.find_by_id('actionRuleTable').first.find_by_text(pack_code)), 1)
    test_helper.assertEqual(browser.find_by_id('actionRuleStatus').text, 'COMPLETED')


@step('the Create Email Template button is clicked on')
def click_create_email_template_button(context):
    context.browser.find_by_id('openCreateEmailTemplateBtn').click()


@step('an email template with packcode "{packcode}", notify service ref "{notify_service_ref}" '
      'and template {template:array} has been created')
def create_email_template(context, packcode, notify_service_ref, template: List):
    context.pack_code = f'{packcode}-' + get_random_alpha_numerics(5)
    context.template = template
    context.notify_template_id = str(uuid.uuid4())

    context.browser.find_by_id('EmailPackcodeTextField').fill(context.pack_code)
    context.browser.find_by_id('EmailDescriptionTextField').fill('email description')
    context.browser.find_by_id('EmailNotifyTemplateIdTextField').fill(context.notify_template_id)
    context.browser.find_by_id('EmailTemplateTextField').fill(str(context.template).replace('\'', '\"'))
    context.browser.find_by_id('EmailNotifyServiceRef').click()
    context.browser.find_by_id(notify_service_ref).click()
    context.browser.find_by_id('createEmailTemplateBtn').click()


@step('I should see the email template in the template list')
def find_created_email_template(context):
    test_helper.assertEqual(
        len(context.browser.find_by_id('emailTemplateTable').first.find_by_text(context.pack_code)), 1)


@step("the email template has been added to the allow on action rule list")
def allow_email_template_on_action_rule(context):
    context.browser.driver.refresh()
    WebDriverWait(context.browser.driver, 30).until(
        EC.element_to_be_clickable((By.ID, 'allowEmailTemplateDialogBtn'))
    ).click()
    context.browser.find_by_id('selectEmailTemplate').click()
    context.browser.find_by_id(context.pack_code, wait_time=30).click()
    context.browser.find_by_id("allowEmailTemplateOnActionRule", wait_time=30).click()


@step('I create an email action rule with email column "{email_column}"')
def click_email_action_rule_button(context, email_column):
    setup_email_action_rule(context, email_column)
    context.browser.find_by_id('createActionRuleBtn').click()


@step('I create an email action rule on the date "{action_rule_date}" with email column "{email_column}"')
def click_email_action_rule_button_with_date(context, action_rule_date, email_column):
    setup_email_action_rule(context, email_column)
    context.browser.find_by_id("triggerDate")[0].value = action_rule_date
    context.browser.find_by_id('createActionRuleBtn').click()


def setup_email_action_rule(context, email_column):
    context.browser.find_by_id('createActionRuleDialogBtn').click()
    context.browser.find_by_id('selectActionRuleType').click()
    context.browser.find_by_value('Email').click()
    context.browser.find_by_id('selectActionRuleEmailPackCode').click()
    context.browser.find_by_id(context.pack_code, wait_time=30).click()
    context.browser.find_by_id('selectActionRuleEmailColumn').click()
    context.browser.find_by_id(email_column, wait_time=30).click()


@step('I can see the Action Rule has been triggered and emails sent to notify api with email column "{email_column}"')
def check_action_rule_triggered_for_email(context, email_column):
    poll_action_rule_completed(context.browser, context.pack_code)
    check_notify_called_with_correct_emails_and_uacs(context, email_column)


@step('I can see the action rule has been created in "{expected_timezone}"')
def check_action_rule_triggered_for_email_in_future(context, expected_timezone):
    action_rule_date_time_str = context.browser.find_by_id('actionRuleDateTime', wait_time=30).text

    if expected_timezone == "GMT":
        action_rule_date_time = datetime.strptime(action_rule_date_time_str, "%d/%m/%Y, %H:%M:%S %Z")
        test_helper.assertIsNone(action_rule_date_time.utcoffset())  # Time is in UTC, so we assert there's no offset
    else:
        action_rule_date_time = datetime.strptime(action_rule_date_time_str, "%d/%m/%Y, %H:%M:%S %Z%z")
        test_helper.assertEqual(action_rule_date_time.utcoffset().seconds, 3600)
