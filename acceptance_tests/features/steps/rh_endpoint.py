from behave import step
from requests import Response
from urllib.parse import parse_qs, urlparse

from acceptance_tests.utilities import jwe_helper, rh_endpoint_client
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

    eq_claims = jwe_helper.decrypt_signed_jwe(query_strings['token'][0])

    test_helper.assertEqual(eq_claims['questionnaire_id'], context.rh_launch_qid,
                            f'Expected to find the correct QID in the claims payload, actual payload: {eq_claims}')
    test_helper.assertEqual(eq_claims['collection_exercise_sid'], context.collex_id,
                            'Expected to find the correct collection exercise ID in the claims payload, '
                            f'actual payload: {eq_claims}')
    test_helper.assertEqual(eq_claims['case_id'], context.emitted_cases[0]['caseId'],
                            f'Expected to find the correct case ID in the claims payload, actual payload: {eq_claims}')

    # Overwrite these values in the context, they are needed for checking the subsequent events
    context.correlation_id = eq_claims['tx_id']
    context.originating_user = eq_claims['user_id']
