from urllib.parse import urlparse, parse_qs

from selenium.webdriver.common.keys import Keys
from behave import step

from acceptance_tests.utilities.jwe_helper import decypting_token_and_asserts
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

RETURN = '\ue006'


@step("the UAC entry page is displayed")
def display_uac_entry_page(context):
    context.browser.visit(f'{Config.RH_UI_URL}en/start')


@step('link text displays string "{expected_displayed_string}"')
def uac_not_valid_displayed(context, expected_displayed_string):
    error_text = context.browser.links.find_by_href('#uac_invalid').text
    test_helper.assertEqual(error_text, expected_displayed_string)


@step('the user enters UAC "{uac}')
def enter_uac(context, uac):
    context.browser.find_by_id('uac').fill(uac)
    context.browser.find_by_id('submitUACBtn').click();

@step("the user enters a valid UAC")
def enter_a_valid_uac(context):
    context.browser.find_by_id('uac').fill(context.rh_launch_uac + RETURN)


@step("they are redirected to EQ")
def is_redirected_to_EQ(context):
    expected_url_start = 'session?token='
    test_helper.assertIn(expected_url_start, context.browser.url)
    query_strings = parse_qs(urlparse(context.browser.url).query)

    test_helper.assertIn('token', query_strings,
                         f'Expected to find launch token in launch URL, actual launch url: {context.browser.url}')
    test_helper.assertEqual(
        len(query_strings['token']), 1,
        f'Expected to find exactly 1 token in the launch URL query stings, actual launch url: {context.browser.url}')

    decypting_token_and_asserts(context, query_strings)


@step("the user enters a receipted UAC")
def input_recipted_uac(context):
    context.browser.find_by_id('uac').fill(context.rh_launch_uac + RETURN)


@step("they are redirected to the receipted page")
def redirected_to_receipted_page(context):
    test_helper.assertIn('This access code has already been used', context.browser.find_by_css('h1').text)


@step("the user enters an inactive UAC")
def enter_inactive_uac(context):
    context.browser.find_by_id('uac').fill(context.rh_launch_uac + RETURN)


@step("they are redirected to the inactive uac page")
def check_on_inactive_uac_page(context):
    test_helper.assertIn('This access code has been marked inactive', context.browser.find_by_css('h1').text)


@step("the user clicks Access Survey without entering a UAC")
def enter_no_uac(context):
    context.browser.find_by_id('uac').fill(RETURN)


@step('An error section is displayed with href "{href_name}" is displayed with "{expected_text}"')
def step_impl(context, href_name, expected_text):
    test_helper.assertEqual(context.browser.find_by_id('error-summary-title').text, 'There is a problem with this page')
    error_text = context.browser.links.find_by_href(href_name).text
    test_helper.assertEqual(error_text, expected_text)