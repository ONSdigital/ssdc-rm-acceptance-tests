
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from behave import step

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("the UAC entry page is displayed")
def display_uac_entry_page(context):
    context.browser.visit(Config.SUPPORT_TOOL_UI_URL)




