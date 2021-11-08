import json
import random
import string
import uuid

import requests
from behave import step

from acceptance_tests.utilities.audit_trail_helper import get_unique_user_email
from acceptance_tests.utilities.event_helper import get_exactly_one_emitted_survey_update
from acceptance_tests.utilities.notify_helper import check_email_fulfilment_response, \
    check_notify_api_called_with_correct_email_and_notify_template_id
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("fulfilments are authorised on email template")
def authorise_sms_pack_code(context):
    url = f'{Config.SUPPORT_TOOL_API}/fulfilmentSurveyEmailTemplates'
    body = {
        'surveyId': context.survey_id,
        'packCode': context.pack_code
    }

    response = requests.post(url, json=body)
    response.raise_for_status()

    survey_update_event = get_exactly_one_emitted_survey_update()

    allowed_email_fulfilments = survey_update_event['allowedEmailFulfilments']
    test_helper.assertEqual(len(allowed_email_fulfilments), 1,
                            'Unexpected number of allowedEmailFulfilments')
    test_helper.assertEqual(allowed_email_fulfilments[0]['packCode'], context.pack_code,
                            'Unexpected allowedEmailFulfilments packCode')


@step('a request has been made for a replacement UAC by email from email address "{email}"')
def request_replacement_uac_by_email(context, email):
    context.email = email
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = get_unique_user_email()

    url = f'{Config.NOTIFY_SERVICE_API}email-fulfilment'
    body = {
        "header": {
            "source": "CC",
            "channel": "CC",
            "correlationId": context.correlation_id,
            "originatingUser": context.originating_user
        },
        "payload": {
            "emailFulfilment": {
                "caseId": context.emitted_cases[0]['caseId'],
                "email": context.email,
                "packCode": context.pack_code,
                'uacMetadata': {"waveOfContact": "1"}
            }
        }
    }

    response = requests.post(url, json=body)
    response.raise_for_status()

    context.email_fulfilment_response_json = response.json()

    check_email_fulfilment_response(context.email_fulfilment_response_json, context.template)


@step("notify api was called with email template")
def check_notify_api_call(context):
    check_notify_api_called_with_correct_email_and_notify_template_id(context.email, context.notify_template_id)


@step("the UAC_UPDATE message matches the email fulfilment UAC")
def check_uac_message_matches_sms_uac(context):
    test_helper.assertEqual(context.emitted_uacs[0]['uacHash'], context.email_fulfilment_response_json['uacHash'],
                            f"Failed to 1st match uacHash, "
                            f"context.emitted_uacs: {context.emitted_uacs} "
                            f" context.email_fulfilment_response_json {context.email_fulfilment_response_json}")

    test_helper.assertEqual(context.emitted_uacs[0]['qid'], context.email_fulfilment_response_json['qid'],
                            f"Failed to 1st match qid, "
                            f"context.emitted_uacs: {context.emitted_uacs} "
                            f"context.email_fulfilment_response_json {context.email_fulfilment_response_json}")


@step('an email template has been created with template "{template}"')
def create_email_template(context, template):
    # By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    context.pack_code = 'pack_code_email_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    context.notify_template_id = str(uuid.uuid4())
    context.template = template
    url = f'{Config.SUPPORT_TOOL_API}/emailTemplates'
    body = {
        'notifyTemplateId': context.notify_template_id,
        'template': json.loads(context.template),
        'packCode': context.pack_code,
        'description': "Test description",
        'metadata': {"foo": "bar"}
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
