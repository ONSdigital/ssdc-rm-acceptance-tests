
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from behave import step


@step("the UAC entry page is displayed")
def display_uac_entry_page(context):
    context.behave_driver.get("http://localhost:9092/en/start/")


@step('page displays string "{expected_displayed_string}"')
def uac_not_valid_displayed(context, expected_displayed_string):
    error_text = context.browser.find_element(By.CLASS_NAME, 'ons-list__link').get_attribute('text')
    assert error_text == expected_displayed_string


@step('the user enters UAC "{uac}')
def enter_uac(context, uac):
    search_input = context.browser.find_element(By.ID, 'uac')
    search_input.send_keys(uac + Keys.RETURN)
