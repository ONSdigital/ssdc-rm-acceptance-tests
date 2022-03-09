import json
import uuid
from datetime import datetime

import requests
from behave import step

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.event_helper import get_exactly_one_emitted_survey_update
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step('a print fulfilment has been requested')
@step('a print fulfilment with personalisation {personalisation:json} has been requested')
def request_print_fulfilment_step(context, personalisation=None):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message_dict = {
        "header": {
            "version": Config.EVENT_SCHEMA_VERSION,
            "topic": Config.PUBSUB_PRINT_FULFILMENT_TOPIC,
            "source": "RH",
            "channel": "RH",
            "dateTime": f'{datetime.utcnow().isoformat()}Z',
            "messageId": str(uuid.uuid4()),
            "correlationId": context.correlation_id,
            "originatingUser": context.originating_user
        },
        "payload": {
            "printFulfilment": {
                "caseId": context.emitted_cases[0]['caseId'],
                "packCode": context.pack_code,
                'uacMetadata': {"foo": "bar"}
            }
        }
    }

    if personalisation:
        context.fulfilment_personalisation = personalisation
        message_dict['payload']['printFulfilment']['personalisation'] = context.fulfilment_personalisation

    message = json.dumps(message_dict)
    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_PRINT_FULFILMENT_TOPIC)
    context.sent_messages.append(message)


@step("export file fulfilments are triggered to be exported")
def print_fulfilments_trigger_step(context):
    url = (f'{Config.SUPPORT_TOOL_API}/fulfilmentNextTriggers/'
           f'?triggerDateTime={datetime.utcnow().replace(microsecond=0).isoformat()}Z')

    response = requests.post(url)
    response.raise_for_status()


@step("fulfilments are authorised on the export file template")
def authorise_pack_code(context):
    url = f'{Config.SUPPORT_TOOL_API}/fulfilmentSurveyExportFileTemplates'
    body = {
        'surveyId': context.survey_id,
        'packCode': context.pack_code
    }

    response = requests.post(url, json=body)
    response.raise_for_status()

    survey_update_event = get_exactly_one_emitted_survey_update()

    allowed_print_fulfilments = survey_update_event['allowedPrintFulfilments']
    test_helper.assertEqual(len(allowed_print_fulfilments), 1,
                            'Unexpected number of allowedPrintFulfilments')
    test_helper.assertEqual(allowed_print_fulfilments[0]['packCode'], context.pack_code,
                            'Unexpected allowedPrintFulfilments packCode')
