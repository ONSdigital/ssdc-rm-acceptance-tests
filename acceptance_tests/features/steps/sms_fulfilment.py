import uuid
from datetime import datetime

import requests
from behave import step

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("fulfilments are authorised on sms template")
def authorise_sms_pack_code(context):
    url = f'{Config.SUPPORT_TOOL_API}/fulfilmentSurveySmsTemplates'
    body = {
        'id': str(uuid.uuid4()),
        'survey': 'surveys/' + context.survey_id,
        'smsTemplate': 'smsTemplates/' + context.pack_code
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


@step('a request has been made for a replacement UAC by SMS from phone number "{phone_number}"')
def request_replacement_uac_by_sms(context, phone_number):
    requests.get(f'{Config.NOTIFY_STUB_SERVICE}/reset')
    context.phone_number = phone_number

    url = f'{Config.NOTIFY_SERVICE_API}sms-fulfilment'
    body = {
        "header": {
            "version": Config.EVENT_SCHEMA_VERSION,
            "topic": Config.PUBSUB_DEACTIVATE_UAC_TOPIC,
            "source": "CC",
            "channel": "CC",
            "dateTime": f'{datetime.utcnow().isoformat()}Z',
            "messageId": str(uuid.uuid4()),
            "correlationId": str(uuid.uuid4()),
            "originatingUser": "foo@bar.com"
        },
        "payload": {
            "smsFulfilment": {
                "caseId": context.emitted_cases[0]['caseId'],
                "phoneNumber": context.phone_number,
                "packCode": context.pack_code,
            }
        }
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


def _check_notify_api_called_with_correct_notify_id(phone_number, notify_id):
    response = requests.get(f'{Config.NOTIFY_STUB_SERVICE}/log')
    test_helper.assertEqual(response.status_code, 200, "Unexpected status code")
    response_json = response.json()
    test_helper.assertEqual(len(response_json), 1, "Incorrect number of responses")
    test_helper.assertEqual(response_json[0]["phone_number"], phone_number, "Incorrect phone number")
    test_helper.assertEqual(response_json[0]["template_id"], notify_id, "Incorrect template Id")


@step("notify api was called with SMS template")
def check_notify_api_call(context):
    _check_notify_api_called_with_correct_notify_id(context.phone_number, context.notify_id)
