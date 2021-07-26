import json
import uuid
from datetime import datetime

import requests
from behave import step

from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.rabbit_helper import publish_json_message
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
    publish_json_message(message, exchange=Config.RABBITMQ_EVENT_EXCHANGE,
                         routing_key=Config.RABBITMQ_FULFILMENT_ROUTING_KEY)


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
