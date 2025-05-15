import json
from urllib.parse import urlparse, parse_qs

from behave import step
from tenacity import wait_fixed, retry, stop_after_delay

from acceptance_tests.features.steps.events_emitted import check_uac_update_msgs_emitted_with_qid_active
from acceptance_tests.features.steps.notify_api import get_uac_from_sms_fulfilment
from acceptance_tests.features.steps.sms_fulfilment import authorise_sms_pack_code, \
    request_replacement_uac_by_sms, check_uac_message_matches_sms_uac
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


@step('the user enters UAC "{uac}"')
def enter_uac(context, uac):
    context.browser.find_by_id('uac').fill(uac)
    context.browser.find_by_id('submit_uac_btn').click()


@step("the user enters a valid UAC")
def enter_a_valid_uac(context):
    context.browser.find_by_id('uac').fill(context.rh_launch_uac + RETURN)


@step('they are redirected to EQ with the correct token and language set to "{language_code}"')
def is_redirected_to_eq(context, language_code):
    eq_claims = _redirect_to_eq(context, language_code)

    context.correlation_id = eq_claims['tx_id']


@step('they are redirected to EQ with the language "{language_code}" and the EQ launch settings file '
      '"{eq_launch_settings_file}"')
def is_redirected_to_eq_with_eq_launch_settings(context, language_code, eq_launch_settings_file=None):
    eq_claims = _redirect_to_eq(context, language_code)

    if eq_launch_settings_file:
        eq_launch_settings_file_path = Config.EQ_LAUNCH_SETTINGS_FILE_PATH.joinpath(eq_launch_settings_file)
        eq_launch_settings = json.loads(eq_launch_settings_file_path.read_text())

        for launch_field in eq_launch_settings:
            test_helper.assertIn(launch_field['launchDataFieldName'], eq_claims['survey_metadata']['data'],
                                 f'Specified metadata not present on eq_claim survey_metadata: {eq_claims}')

    context.correlation_id = eq_claims['tx_id']


@step("the user enters a receipted UAC")
def input_receipted_uac(context):
    context.browser.find_by_id('uac').fill(context.rh_launch_uac + RETURN)


@step("they are redirected to the receipted page")
@retry(wait=wait_fixed(2), stop=stop_after_delay(30))
def redirected_to_receipted_page(context):
    test_helper.assertIn('This access code has already been used', context.browser.find_by_css('h1').text)


@step("the user enters an inactive UAC")
def enter_inactive_uac(context):
    context.browser.find_by_id('uac').fill(context.rh_launch_uac + RETURN)


@step("they are redirected to the inactive uac page")
@retry(wait=wait_fixed(2), stop=stop_after_delay(30))
def check_on_inactive_uac_page(context):
    test_helper.assertIn('This questionnaire has now closed', context.browser.find_by_css('h1').text)


@step("the user clicks Access Survey without entering a UAC")
def enter_no_uac(context):
    context.browser.find_by_id('uac').fill(RETURN)


@step('check UAC is in firestore via eqLaunched endpoint for the correct "{language_code}"')
def check_uac_in_firestore(context, language_code):
    context.rh_launch_endpoint_response = rh_endpoint_client.post_to_launch_endpoint(language_code,
                                                                                     context.rh_launch_uac)
    eq_claims = check_launch_redirect_and_get_eq_claims(context.rh_launch_endpoint_response,
                                                        context.rh_launch_qid,
                                                        context.emitted_cases[0]['caseId'],
                                                        context.collex_id,
                                                        context.collex_end_date,
                                                        language_code)
    context.correlation_id = eq_claims['tx_id']
    check_uac_update_msgs_emitted_with_qid_active_and_field_equals_value(context.emitted_cases, context.correlation_id,
                                                                         True, "eqLaunched", True,
                                                                         context.test_start_utc_datetime)


@step('an error section is headed "{error_section_header}" and href "{href_name}" is "{expected_text}"')
def error_section_displayed_with_header_text(context, error_section_header, href_name, expected_text):
    test_helper.assertEqual(context.browser.find_by_id('alert').text, error_section_header)
    error_text = context.browser.links.find_by_href(href_name).text
    test_helper.assertEqual(error_text, expected_text)


@retry(wait=wait_fixed(2), stop=stop_after_delay(30))
def _redirect_to_eq(context, language_code):
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
                                                        context.collex_end_date,
                                                        query_strings['token'][
                                                            0], language_code)
    return eq_claims


@step('and we request a UAC by SMS and the UAC is ready and RH page has "{expected_text}" for "{language_code}"')
def we_request_a_UAC_via_SMS_and_check_the_UAC_in_firestore_and_page_is_ready(context, expected_text, language_code):
    authorise_sms_pack_code(context, 'uac__qid')
    request_replacement_uac_by_sms(context, "07123456789")
    check_uac_update_msgs_emitted_with_qid_active(context, True)
    check_uac_message_matches_sms_uac(context)
    get_uac_from_sms_fulfilment(context)
    check_uac_in_firestore(context, language_code)
    display_uac_entry_page_for_language_and_contains_heading(context, language_code, expected_text)
