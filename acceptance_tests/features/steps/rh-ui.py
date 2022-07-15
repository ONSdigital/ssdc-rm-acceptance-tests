from behave import *
from splinter import Browser

use_step_matcher("re")


@given("I've opened RH-UI")
def open_rh_ui(context):
    browser = Browser()  # defaults to firefox
    browser.visit('http://google.com')
    browser.fill('q', 'splinter - python acceptance testing for web applications')
    browser.find_by_name('btnK').click()

    if browser.is_text_present('splinter.readthedocs.io'):
        print("Yes, the official website was found!")
    else:
        print("No, it wasn't found... We need to improve our SEO techniques")

    browser.quit()
