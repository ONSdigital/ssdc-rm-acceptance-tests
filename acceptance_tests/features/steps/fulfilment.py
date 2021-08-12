import json
import uuid
from datetime import datetime
from time import sleep

import requests
from behave import step

from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step('a print fulfilment has been requested')
def request_print_fulfilment_step(context):
    message = json.dumps(
        {
            "event": {
                "type": "FULFILMENT",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2021-06-09T13:49:19.716761Z",
                "transactionId": "92df974c-f03e-4519-8d55-05e9c0ecea43"
            },
            "payload": {
                "fulfilment": {
                    "caseId": context.emitted_cases[0]['caseId'],
                    "packCode": context.pack_code
                }
            }
        })
    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_FULFILMENT_TOPIC)

    # TODO - maybe trigger the fulfilments a few seconds in the future instead, but this should work for now, I hope!
    sleep(2)


@step('print fulfilments are triggered to be sent for printing')
def print_fulfilments_trigger_step(context):
    with open_cursor() as cur:
        add_trigger_query = """INSERT INTO casev3.fulfilment_next_trigger (id, trigger_date_time) VALUES(%s,%s)"""
        trigger_vars = (str(uuid.uuid4()), datetime.utcnow())
        cur.execute(add_trigger_query, vars=trigger_vars)


@step("fulfilments are authorised on print template")
def authorise_pack_code(context):
    url = f'{Config.SUPPORT_TOOL_API}/fulfilmentSurveyPrintTemplates'
    body = {
        'id': str(uuid.uuid4()),
        'survey': 'surveys/' + context.survey_id,
        'printTemplate': 'printTemplates/' + context.pack_code
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


@step("fulfilments are authorised on sms template")
def authorise_pack_code(context):
    url = f'{Config.SUPPORT_TOOL_API}/fulfilmentSurveySmsTemplates'
    body = {
        'id': str(uuid.uuid4()),
        'survey': 'surveys/' + context.survey_id,
        'smsTemplate': 'smsTemplates/' + context.pack_code
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


@step("a request has been made for a replacement UAC by SMS by the phone number \"{phone_number}\"")
def request_replacement_uac_by_sms(context, phone_number):
    requests.get(f'{Config.NOTIFY_STUB_SERVICE}/reset')
    url = f'{Config.NOTIFY_SERVICE_API}sms-fulfilment'
    body = {
        "event": {
            "type": "SMS_FULFILMENT",
            "source": "CC",
            "channel": "CC",
            "dateTime": "2021-06-09T13:49:19.716761Z",
            "transactionId": "92df974c-f03e-4519-8d55-05e9c0ecea43"
        },
        "payload": {
            "smsFulfilment": {
                "caseId": context.emitted_cases[0]['caseId'],
                "phoneNumber": phone_number,
                "packCode": context.pack_code,
            }
        }
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
