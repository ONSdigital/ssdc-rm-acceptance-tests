
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
    assert error_text == expected_displayed_string


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
