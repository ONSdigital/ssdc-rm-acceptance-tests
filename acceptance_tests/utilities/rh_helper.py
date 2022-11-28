from requests import Response

from acceptance_tests.utilities.jwe_helper import decrypt_claims_token_and_check_contents
from acceptance_tests.utilities.test_case_helper import test_helper
from urllib.parse import parse_qs, urlparse


def check_launch_redirect_and_get_eq_claims(rh_launch_endpoint_response, rh_launch_qid, case_id, collex_id,
                                            language_code, expected_launch_data_list=None):
    response: Response = rh_launch_endpoint_response
    test_helper.assertTrue(response.is_redirect, 'Expected RH response to redirect to EQ launch')

    launch_url = response.next.url
    query_strings = parse_qs(urlparse(launch_url).query)

    test_helper.assertIn('token', query_strings,
                         f'Expected to find launch token in launch URL, actual launch url: {launch_url}')
    test_helper.assertEqual(
        len(query_strings['token']), 1,
        f'Expected to find exactly 1 token in the launch URL query stings, actual launch url: {launch_url}')

    return decrypt_claims_token_and_check_contents(rh_launch_qid,
                                                   case_id,
                                                   collex_id,
                                                   query_strings['token'][0],
                                                   language_code,
                                                   expected_launch_data_list)
