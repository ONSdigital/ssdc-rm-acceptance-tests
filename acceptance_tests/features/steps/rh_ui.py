from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from behave import step

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("the UAC entry page is displayed")
def display_uac_entry_page(context):
    context.behave_driver.get(Config.RH_UI_URL)


@step('link text displays string "{expected_displayed_string}"')
def uac_not_valid_displayed(context, expected_displayed_string):
    error_text = context.behave_driver.find_element(By.CLASS_NAME, 'ons-list__link').get_attribute('text')
    test_helper.assertEqual(error_text, expected_displayed_string)


@step('the user enters UAC "{uac}')
def enter_uac(context, uac):
    search_input = context.behave_driver.find_element(By.ID, 'uac')
    search_input.send_keys(uac + Keys.RETURN)


@step("I use the survey Id to click on the created survey")
def click_on_survey_by_id(context):
    xpath = f'//a[contains(@href, "{context.survey_id}")]'
    survey_link = context.behave_driver.find_element_by_xpath(xpath)
    survey_link.click()


@step('I open the page "{url}"')
def open_page(context, url):
    context.behave_driver.get(url)


@step('page displays string "{expected_text}"')
def page_contains_text(context, expected_text):
    test_helper.assertIn(expected_text, context.behave_driver.page_source)


@step("I navigate to support tool home")
def open_support_tool_home(context):
    context.behave_driver.get(Config.SUPPORT_TOOL_UI_URL)


@step("the user enters a valid UAC")
def enter_a_valid_uac(context):
    search_input = context.behave_driver.find_element(By.ID, 'uac')
    search_input.send_keys(context.uacs_from_actual_export_file[0] + Keys.RETURN)


@step("they are redirected to EQ")
def is_directed_to_EQ(context):
    expected_url_start = f'{Config.EQ_URL}session?token='
    test_helper.assertIn(expected_url_start, context.behave_driver.current_url)
    #  Check token here with some magic code


@step("the user enters a receipted UAC")
def input_recipted_uac(context):
    search_input = context.behave_driver.find_element(By.ID, 'uac')
    search_input.send_keys(context.uacs_from_actual_export_file[0] + Keys.RETURN)


@step("they are redirected to the receipted page")
def redirected_to_receipted_page(context):
    test_helper.assertIn('Someone has already submitted a response using this access code',
                         context.behave_driver.page_source)


@step("the user enters an inactive UAC")
def enter_inactive_uac(context):
    search_input = context.behave_driver.find_element(By.ID, 'uac')
    search_input.send_keys(context.uacs_from_actual_export_file[0] + Keys.RETURN)


@step("they are redirected to the inactive uac page")
def check_on_inactive_uac_page(context):
    test_helper.assertIn('This access code has been marked inactive', context.behave_driver.page_source)


@step("the user clicks Access Survey without entering a UAC")
def enter_no_uac(context):
    search_input = context.behave_driver.find_element(By.ID, 'uac')
    search_input.send_keys(Keys.RETURN)