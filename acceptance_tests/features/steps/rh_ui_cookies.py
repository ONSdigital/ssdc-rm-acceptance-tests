from behave import step

import json

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

RETURN = "\ue006"


@step("the cookies page is displayed")
def display_uac_cookies_page(context):
    context.browser.visit(f"{Config.RH_UI_URL}en/cookies")


# Cookies banner checks and interactions


@step("the cookies banner is displayed")
def display_cookies_banner(context):
    context.browser.find_by_id("ons-cookies-banner")


@step("the user {action} the cookies on the cookies banner")
def select_cookies_on_cookies_banner(context, action):
    button_class = (
        "ons-js-accept-cookies" if action == "accepts" else "ons-js-reject-cookies"
    )

    xpath_string = f'//button[contains(@class,"{button_class}")]'
    context.browser.find_by_xpath(xpath_string).click()


@step("the 'View cookies' hyperlink points to {expected_path}")
def assert_view_cookies_link_on_banner_points_to_cookies_page(context, expected_path):
    xpath_string = '//a[@class="ons-cookies-banner__link" and text()="View cookies"]'
    link = context.browser.find_by_xpath(xpath_string).first
    test_helper.assertEqual(link["href"], f"{Config.RH_UI_URL}{expected_path}")


@step("the 'cookies' hyperlink on the cookies banner points to {expected_path}")
def assert_cookies_hyperlinked_text_on_banner_points_to_cookies_page(
    context, expected_path
):
    xpath_string = '//div[@class="ons-cookies-banner__statement"]/a[text()=" cookies."]'
    link = context.browser.find_by_xpath(xpath_string)
    test_helper.assertEqual(link["href"], f"{Config.RH_UI_URL}{expected_path}")


@step('the "change cookie preferences" hyperlink text points to {expected_path}')
def assert_change_cookie_preferences_link_on_banner_points_to_cookies_page(
    context, expected_path
):
    xpath_string = '//span[@class="ons-cookies-banner__preferences-text"]/a[text()=" change your cookie preferences"]'
    link = context.browser.find_by_xpath(xpath_string)
    test_helper.assertEqual(link["href"], f"{Config.RH_UI_URL}{expected_path}")


# Cookies page radio interactions


@step("the user sets the selection under {para_title} to {cookie_selection}")
def update_cookie_selection_radio(context, para_title, cookie_selection):
    match para_title:
        case "Cookies that measure website use":
            name_attribute_value = "cookies-usage"
        case "Cookies that help with our communications":
            name_attribute_value = "cookies-campaigns"
        case "Cookies that remember your settings":
            name_attribute_value = "cookies-settings"
        case _:
            test_helper.fail(f"Found unexpected cookies paragraph title: {para_title}")

    xpath_string = f'//input[@name="{name_attribute_value}" and @value="{cookie_selection.lower()}"]'
    context.browser.find_by_xpath(xpath_string).first.click()

    submit_button_xpath_string = '//button[@type="submit"]'
    context.browser.find_by_xpath(submit_button_xpath_string).click()


# Checking cookie values


@step(
    "the field {cookie_key} within the ons_cookie_policy cookie is set to {cookie_selection}"
)
def assert_ons_cookie_policy_selection(context, cookie_key, cookie_selection):
    cookies_dict = context.browser.cookies.all()
    ons_cookie_policy_dict = _parse_ons_cookie_policy_json_string(
        cookies_dict["ons_cookie_policy"]
    )

    actual_value = ons_cookie_policy_dict[cookie_key]
    expected_value = True if cookie_selection == "On" else False

    test_helper.assertEqual(actual_value, expected_value)


@step("all optional cookies are set to {cookie_selection}")
def assert_optional_cookie_selection(context, cookie_selection):
    cookies_dict = context.browser.cookies.all()
    ons_cookie_policy_dict = _parse_ons_cookie_policy_json_string(
        cookies_dict["ons_cookie_policy"]
    )

    expected_value = True if cookie_selection == "On" else False

    for cookie_key in ons_cookie_policy_dict:
        if cookie_key != "essential":
            test_helper.assertEqual(ons_cookie_policy_dict[cookie_key], expected_value)


def _parse_ons_cookie_policy_json_string(ons_cookie_policy_string) -> dict:
    ons_cookie_policy_string = ons_cookie_policy_string.replace("'", '"')
    ons_cookie_policy_dict = json.loads(ons_cookie_policy_string)

    return ons_cookie_policy_dict
