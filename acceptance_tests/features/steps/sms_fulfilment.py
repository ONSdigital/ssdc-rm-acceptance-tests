import json
import random
import string
import uuid

import requests
from behave import step

from acceptance_tests.utilities.audit_trail_helper import get_unique_user_email
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
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = get_unique_user_email()

    url = f'{Config.NOTIFY_SERVICE_API}sms-fulfilment'
    body = {
        "header": {
            "source": "CC",
            "channel": "CC",
            "correlationId": context.correlation_id,
            "originatingUser": context.originating_user
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

    context.sms_fulfilment_response_json = response.json()

    _check_sms_fulfilment_response(context.sms_fulfilment_response_json, context.template)


def _check_notify_api_called_with_correct_notify_template_id(phone_number, notify_template_id):
    response = requests.get(f'{Config.NOTIFY_STUB_SERVICE}/log')
    test_helper.assertEqual(response.status_code, 200, "Unexpected status code")
    response_json = response.json()
    test_helper.assertEqual(len(response_json), 1, f"Incorrect number of responses, response json {response_json}")
    test_helper.assertEqual(response_json[0]["phone_number"], phone_number, "Incorrect phone number, "
                                                                            f'response json {response_json}')
    test_helper.assertEqual(response_json[0]["template_id"], notify_template_id,
                            f"Incorrect Gov Notify template Id, response json {response_json}")


@step("notify api was called with SMS template")
def check_notify_api_call(context):
    _check_notify_api_called_with_correct_notify_template_id(context.phone_number, context.notify_template_id)


@step("the UAC_UPDATE message matches the SMS fulfilment UAC")
def check_uac_message_matches_sms_uac(context):
    test_helper.assertEqual(context.emitted_uacs[0]['uacHash'], context.sms_fulfilment_response_json['uacHash'],
                            f"Failed to 1st match uacHash, "
                            f"context.emitted_uacs: {context.emitted_uacs} "
                            f" context.sms_fulfilment_response_json {context.sms_fulfilment_response_json}")

    test_helper.assertEqual(context.emitted_uacs[0]['qid'], context.sms_fulfilment_response_json['qid'],
                            f"Failed to 1st match qid, "
                            f"context.emitted_uacs: {context.emitted_uacs} "
                            f"context.sms_fulfilment_response_json {context.sms_fulfilment_response_json}")


@step('a sms template has been created with template "{template}"')
def create_sms_template(context, template):
    # By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    context.pack_code = 'pack_code_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    context.notify_template_id = str(uuid.uuid4())
    context.template = template
    url = f'{Config.SUPPORT_TOOL_API}/smsTemplates'
    body = {
        'notifyTemplateId': context.notify_template_id,
        'template': json.loads(context.template),
        'packCode': context.pack_code
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


def _check_sms_fulfilment_response(sms_fulfilment_response, template):
    expect_uac_hash_and_qid_in_response = any(
        template_item in json.loads(template) for template_item in ['__qid__', '__uac__'])

    if expect_uac_hash_and_qid_in_response:
        test_helper.assertTrue(sms_fulfilment_response['uacHash'],
                               f"sms_fulfilment_response uacHash not found: {sms_fulfilment_response}")
        test_helper.assertTrue(sms_fulfilment_response['qid'],
                               f"sms_fulfilment_response qid not found: {sms_fulfilment_response}")
    else:
        test_helper.assertFalse(
            sms_fulfilment_response)  # Empty JSON is expected response for non-UAC/QID template
