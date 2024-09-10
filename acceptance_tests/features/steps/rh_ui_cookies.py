from behave import step

import json

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

RETURN = "\ue006"


@step("the cookies page is displayed")
def display_uac_cookies_page(context):
    context.browser.visit(f"{Config.RH_UI_URL}en/cookies")


# Cookies banner


@step("the cookies banner is displayed")
def display_cookies_banner(context):
    context.browser.cookies.delete_all()  # clear cookies to ensure that the banner is displayed
    context.browser.find_by_id("ons-cookies-banner")


@step("the user accepts the cookies on the cookies banner")
def accept_cookies_on_cookies_banner(context):
    xpath_string = '//button[contains(@class,"ons-js-accept-cookies")]'
    context.browser.find_by_xpath(xpath_string).click()


@step("the user rejects the cookies on the cookies banner")
def reject_cookies_on_cookies_banner(context):
    xpath_string = '//button[contains(@class,"ons-js-reject-cookies")]'
    context.browser.find_by_xpath(xpath_string).click()


@step("the user clicks the View cookies link")
def click_view_cookies_link_on_banner(context):
    context.browser.find_by_id("ons-cookies-banner__link").click()


@step('the user clicks the "cookies" hyperlink text')
def click_cookies_hyperlinked_text_on_banner(context):
    xpath_string = '//div[@class="ons-cookies-banner__statement"]/a[text()=" cookies."]'
    context.browser.find_by_xpath(xpath_string).click()


@step('the user clicks the "change cookie preferences" hyperlink text')
def click_change_cookie_preferences_link_on_banner(context):
    xpath_string = '//span[@class="ons-cookies-banner__preferences-text"]/a[text()=" change your cookie preferences"]'
    context.browser.find_by_path(xpath_string).click()


# Cookies page radio interactions


@step("the user sets the selection under {para_title} to {cookie_selection}")
def change_cookies_selection(context, para_title, cookie_selection):
    match para_title:
        case "Cookies that measure website use":
            name_attribute_value = "cookies-usage"
        case "Cookies that help with our communications":
            name_attribute_value = "cookies-campaigns"
        case "Cookies that remember your settings":
            name_attribute_value = "cookies-settings"

    # breakpoint()

    # _css_version(context, name_attribute_value, cookie_selection)

    cookies_dict = context.browser.cookies.all()
    ons_cookie_policy_string = cookies_dict["ons_cookie_policy"]
    print(f"THE COOKIE: {ons_cookie_policy_string}")


def _xpath_version(context, name_attribute_value, cookie_selection):
    xpath_string = f'//input[@name="{name_attribute_value}" and @value="{cookie_selection.lower()}"]'
    context.browser.find_by_xpath(xpath_string).first.click()

    print(f"XPATH: {xpath_string}")


def _css_version(context, name_attribute_value, cookie_selection):
    css_string = f'[type="radio"][value="{cookie_selection.lower()}"][name="{name_attribute_value}"]'
    print(context.browser.find_by_css(css_string))
    context.browser.find_by_css(css_string).first.click()


def _id_version(context, name_attribute_value, cookie_selection):
    match name_attribute_value:
        case "cookies-usage":
            id = "off-1"
        case "cookies-campaigns":
            id = "off-2"
        case "cookies-settings":
            id = "off-3"

    context.browser.find_by_id(id).first.click()


def _splinter_choose_version(context, name_attribute_value, cookie_selection):

    # context.browser.choose("cookies-usage", "off")
    context.browser.choose(name_attribute_value, cookie_selection)


def _splinter_fill_form_version(context):
    context.browser.choose("cookies-usage", "off")


# Cookie value


@step(
    "the field {cookie_key} within the ons_cookie_policy cookie is set to {cookie_selection}"
)
def assert_ons_cookie_policy(context, cookie_key, cookie_selection):
    context.browser.reload()  # reload to ensure the selection has been propagated

    cookies_dict = context.browser.cookies.all()

    ons_cookie_policy_string = cookies_dict["ons_cookie_policy"]
    ons_cookie_policy_string = ons_cookie_policy_string.replace("'", '"')
    ons_cookie_policy_dict = json.loads(ons_cookie_policy_string)

    actual_value = ons_cookie_policy_dict[cookie_key]
    expected_value = True if cookie_selection == "On" else False

    test_helper.assertEqual(actual_value, expected_value)


@step("all optional cookies are set to {cookie_selection}")
def assert_bulk_optional_cookie_selection(context, cookie_selection):
    expected_value = True if cookie_selection == "On" else False
    cookies_dict = context.browser.cookies.all()
    ons_cookie_policy_dict = cookies_dict["ons_cookie_policy"]

    for cookie_key in ons_cookie_policy_dict:
        if cookie_key != "essential":
            test_helper.assertEqual(ons_cookie_policy_dict[cookie_key], expected_value)
