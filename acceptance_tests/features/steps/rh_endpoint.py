from behave import step
from requests import Response
from urllib.parse import parse_qs, urlparse

from acceptance_tests.utilities import rh_endpoint_client
from acceptance_tests.utilities.jwe_helper import decrypt_claims_token_and_check_contents
from acceptance_tests.utilities.test_case_helper import test_helper


@step('the respondent home UI launch endpoint is called with the UAC')
def post_rh_launch_endpoint(context):
    context.rh_launch_endpoint_response = rh_endpoint_client.post_to_launch_endpoint(context.rh_launch_uac)


@step('it redirects to a launch URL with a launch claims token')
def check_launch_redirect_and_token(context):
    response: Response = context.rh_launch_endpoint_response
    test_helper.assertTrue(response.is_redirect, 'Expected RH response to redirect to EQ launch')

    launch_url = response.next.url
    query_strings = parse_qs(urlparse(launch_url).query)

    test_helper.assertIn('token', query_strings,
                         f'Expected to find launch token in launch URL, actual launch url: {launch_url}')
    test_helper.assertEqual(
        len(query_strings['token']), 1,
        f'Expected to find exactly 1 token in the launch URL query stings, actual launch url: {launch_url}')

    context.correlation_id, context.originating_user = decrypt_claims_token_and_check_contents(context.rh_launch_qid,
                                                                                               context.emitted_cases[0][
                                                                                                   'caseId'],
                                                                                               context.collex_id,
                                                                                               query_strings['token'][
                                                                                                   0])
