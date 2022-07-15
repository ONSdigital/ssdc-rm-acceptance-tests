from behave import *
from splinter import Browser

use_step_matcher("re")


@given("I've opened RH-UI")
def open_rh_ui(context):
    browser = Browser()  # defaults to firefox
    browser.visit('https://stackoverflow.com/questions/39488311/python-reproduce-splinter-selenium-behaviour-for-testing-a-website-that-uses-j')

    if browser.is_text_present('class ScreenShotListener(AbstractEventListener'):
        print("good")
    else:
        print("bad")

    browser.quit()
