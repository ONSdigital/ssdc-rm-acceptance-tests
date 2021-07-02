import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.database_helper import open_write_cursor
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
                    "caseId": context.emitted_cases_id[0],
                    "fulfilmentCode": context.unique_template_code
                }
            }
        })
    publish_json_message(message, routing_key=Config.RABBITMQ_FULFILMENT_QUEUE)


@step('a print fulfilment template has been created with template "{template}" and print supplier "{supplier}"')
def print_fulfilment_template_step(context, template, supplier):
    with open_write_cursor() as cur:
        add_template_query = """INSERT INTO casev3.fulfilment_template
                                (fulfilment_code, template, print_supplier) VALUES(%s,%s,%s)"""
        context.unique_template_code = 'AT_TEMPLATE_' + str(uuid.uuid4())
        context.template = template
        context.pack_code = context.unique_template_code
        template_vars = (context.unique_template_code, template, supplier)
        cur.execute(add_template_query, vars=template_vars)


@step('print fulfilments are triggered to be sent for printing')
def print_fulfilments_trigger_step(context):
    with open_write_cursor() as cur:
        add_trigger_query = """INSERT INTO casev3.fulfilment_next_trigger (id, trigger_date_time) VALUES(%s,%s)"""
        trigger_vars = (str(uuid.uuid4()), datetime.utcnow())
        cur.execute(add_trigger_query, vars=trigger_vars)
