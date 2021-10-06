import requests
from behave import step

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step('there is a request for telephone capture of a case')
def request_telephone_capture(context):
    body = {
        "foo": "bar"
    }

    response = requests.post(f"{Config.CASE_API_CASE_URL}{context.emitted_cases[0]['caseId']}/telephone-capture",
                             json=body)
    response.raise_for_status()
    context.telephone_capture_request = response.json()


@step('a UAC and QID with questionnaire type "{qid_type}" type are generated and returned')
def check_telephone_capture_generated(context, qid_type):
    test_helper.assertIsNotNone(context.telephone_capture_request.get('uac'),
                                'The telephone capture response must include a UAC, '
                                f'context.telephone_capture_request: {context.telephone_capture_request}')
    test_helper.assertEqual(context.telephone_capture_request['qid'][:2], qid_type,
                            'The telephone capture response must include a QID of the expected type '
                            f'context.telephone_capture_request: {context.telephone_capture_request}')
    test_helper.assertEqual(context.telephone_capture_request.get('uacMetadata'), {'foo': 'bar'})
