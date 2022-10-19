from urllib.parse import urlparse, parse_qs

from behave import step

from acceptance_tests.utilities import rh_endpoint_client
from acceptance_tests.utilities.event_helper import check_uac_update_msgs_emitted_with_qid_active_and_field_equals_value
from acceptance_tests.utilities.jwe_helper import decrypt_claims_token_and_check_contents
from acceptance_tests.utilities.rh_helper import check_launch_redirect_and_get_eq_claims
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

RETURN = '\ue006'


@step("the UAC entry page is displayed")
def display_uac_entry_page(context):
    context.browser.visit(f'{Config.RH_UI_URL}en/start')


@step('the UAC entry page is displayed for "{language_code}"')
def display_uac_entry_page_for_language(context, language_code):
    context.browser.visit(f'{Config.RH_UI_URL}{language_code}/start')


@step('the UAC entry page is titled "{expected_text}" and is displayed for "{language_code}"')
def display_uac_entry_page_for_language_and_contains_heading(context, language_code, expected_text):
    context.browser.visit(f'{Config.RH_UI_URL}{language_code}/start')
    text = context.browser.title
    test_helper.assertEqual(text, expected_text)


@step('link text displays string "{expected_displayed_string}"')
def uac_not_valid_displayed(context, expected_displayed_string):
    error_text = context.browser.links.find_by_href('#uac_invalid').text
    test_helper.assertEqual(error_text, expected_displayed_string)


@step('the user enters UAC "{uac}')
def enter_uac(context, uac):
    context.browser.find_by_id('uac').fill(uac)
    context.browser.find_by_id('submit_uac_btn').click()


@step("the user enters a valid UAC")
def enter_a_valid_uac(context):
    context.browser.find_by_id('uac').fill(context.rh_launch_uac + RETURN)


@step('they are redirected to EQ with the correct token and language set to "{language_code}"')
def is_redirected_to_EQ(context, language_code):
    expected_url_start = 'session?token='
    test_helper.assertIn(expected_url_start, context.browser.url)
    query_strings = parse_qs(urlparse(context.browser.url).query)

    test_helper.assertIn('token', query_strings,
                         f'Expected to find launch token in launch URL, actual launch url: {context.browser.url}')
    test_helper.assertEqual(
        len(query_strings['token']), 1,
        f'Expected to find exactly 1 token in the launch URL query stings, actual launch url: {context.browser.url}')

    eq_claims = decrypt_claims_token_and_check_contents(context.rh_launch_qid,
                                                        context.emitted_cases[0][
                                                            'caseId'],
                                                        context.collex_id,
                                                        query_strings['token'][
                                                            0], language_code)

    context.correlation_id = eq_claims['tx_id']


@step("the user enters a receipted UAC")
def input_receipted_uac(context):
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


@step('an error section is displayed with href "{href_name}" is displayed with "{expected_text}"')
def error_section_displayed(context, href_name, expected_text):
    test_helper.assertEqual(context.browser.find_by_id('alert').text, 'There is a problem with this page')
    error_text = context.browser.links.find_by_href(href_name).text
    test_helper.assertEqual(error_text, expected_text)


@step('check UAC is in firestore via eqLaunched endpoint for the correct "{language_code}"')
def check_uac_in_firestore(context, language_code):
    context.rh_launch_endpoint_response = rh_endpoint_client.post_to_launch_endpoint(language_code,
                                                                                     context.rh_launch_uac)
    eq_claims = check_launch_redirect_and_get_eq_claims(context.rh_launch_endpoint_response,
                                                        context.rh_launch_qid,
                                                        context.emitted_cases[0]['caseId'],
                                                        context.collex_id,
                                                        language_code)
    context.correlation_id = eq_claims['tx_id']
    check_uac_update_msgs_emitted_with_qid_active_and_field_equals_value(context.emitted_cases, context.correlation_id,
                                                                         True, "eqLaunched", True)


@step('an error section is headed "{error_section_header}" and href "{href_name}" is "{expected_text}"')
def error_section_displayed_with_header_text(context, error_section_header, href_name, expected_text):
    test_helper.assertEqual(context.browser.find_by_id('alert').text, error_section_header)
    error_text = context.browser.links.find_by_href(href_name).text
    test_helper.assertEqual(error_text, expected_text)
