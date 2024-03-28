import uuid

import requests
from behave import step

from acceptance_tests.utilities import iap_requests
from acceptance_tests.utilities.audit_trail_helper import get_unique_user_email
from acceptance_tests.utilities.event_helper import get_emitted_survey_update_by_id
from acceptance_tests.utilities.notify_helper import check_email_fulfilment_response
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step('fulfilments are authorised for email template "{template_name}"')
def authorise_sms_pack_code(context, template_name):
    context.template = context.email_templates[template_name]['template']
    context.pack_code = context.email_packcodes[template_name]['pack_code']
    context.notify_template_id = context.email_packcodes[template_name]['notify_template_id']

    url = f'{Config.SUPPORT_TOOL_API}/fulfilmentSurveyEmailTemplates'
    body = {
        'surveyId': context.survey_id,
        'packCode': context.pack_code
    }

    response = iap_requests.make_request(method='POST', url=url, json=body)
    response.raise_for_status()

    survey_update_event = get_emitted_survey_update_by_id(context.survey_id, context.test_start_utc_datetime)

    allowed_email_fulfilments = survey_update_event['allowedEmailFulfilments']
    test_helper.assertEqual(len(allowed_email_fulfilments), 1,
                            'Unexpected number of allowedEmailFulfilments')
    test_helper.assertEqual(allowed_email_fulfilments[0]['packCode'], context.pack_code,
                            'Unexpected allowedEmailFulfilments packCode')


@step('a request has been made for a replacement UAC by email from email address "{email}"')
@step('a request has been made for a replacement UAC by email from email address "{email}"'
      ' with personalisation {personalisation:json}')
def request_replacement_uac_by_email(context, email, personalisation=None):
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

    if personalisation:
        context.fulfilment_personalisation = body['payload']['emailFulfilment']['personalisation'] = personalisation

    response = iap_requests.make_request(method='POST', url=url, json=body)
    response.raise_for_status()

    context.fulfilment_response_json = response.json()

    check_email_fulfilment_response(context.fulfilment_response_json, context.template)


@step("the UAC_UPDATE message matches the email fulfilment UAC")
def check_uac_message_matches_email_uac(context):
    test_helper.assertEqual(context.emitted_uacs[0]['uacHash'], context.fulfilment_response_json['uacHash'],
                            f"Failed to 1st match uacHash, "
                            f"context.emitted_uacs: {context.emitted_uacs} "
                            f" context.fulfilment_response_json {context.fulfilment_response_json}")

    test_helper.assertEqual(context.emitted_uacs[0]['qid'], context.fulfilment_response_json['qid'],
                            f"Failed to 1st match qid, "
                            f"context.emitted_uacs: {context.emitted_uacs} "
                            f"context.fulfilment_response_json {context.fulfilment_response_json}")


@step('an email template has been created with template "{template_name}"')
def create_email_template(context, template_name):
    context.template = context.email_templates[template_name]['template']
    context.pack_code = context.email_packcodes[template_name]['pack_code']
    context.notify_template_id = context.email_packcodes[template_name]['notify_template_id']
