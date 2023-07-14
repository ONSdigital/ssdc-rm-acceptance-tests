from behave import step
from acceptance_tests.utilities import rh_endpoint_client
from acceptance_tests.utilities.rh_helper import check_launch_redirect_and_get_eq_claims


@step('the respondent home UI launch endpoint is called with the UAC')
def post_rh_launch_endpoint(context):
    context.rh_launch_endpoint_response = rh_endpoint_client.post_to_launch_endpoint('en', context.rh_launch_uac)


@step('it redirects to a launch URL with a launch claims token')
def check_launch_redirect_and_token(context):
    eq_claims = check_launch_redirect_and_get_eq_claims(context.rh_launch_endpoint_response,
                                                        context.rh_launch_qid,
                                                        context.emitted_cases[0]['caseId'],
                                                        context.collex_id,
                                                        context.collex_end_date,
                                                        'en')
    context.correlation_id = eq_claims['tx_id']
    context.eq_launch_claims = eq_claims
