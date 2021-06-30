import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.database_helper import open_write_cursor
from acceptance_tests.utilities.rabbit_context import RabbitContext
from config import Config


@step('a fulfilment has been requested')
def request_fulfilment_step(context):
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
                    "caseId": context.loaded_case_ids[0],
                    "fulfilmentCode": context.unique_template_code
                }
            }
        })

    with RabbitContext(exchange='') as rabbit:
        rabbit.publish_message(
            message=message,
            content_type='application/json',
            routing_key=Config.RABBITMQ_FULFILMENT_QUEUE)


@step('a fulfilment template has been created with template "{template}" and print supplier "{supplier}"')
def fulfilment_template_step(context, template, supplier):
    with open_write_cursor() as cur:
        add_template_query = """INSERT INTO casev3.fulfilment_template
                                (fulfilment_code, template, print_supplier) VALUES(%s,%s,%s)"""
        context.unique_template_code = 'AT_TEMPLATE_' + str(uuid.uuid4())
        context.template = template
        context.pack_code = context.unique_template_code
        template_vars = (context.unique_template_code, template, supplier)
        cur.execute(add_template_query, vars=template_vars)


@step('fulfilments trigger')
def fulfilments_trigger_step(context):
    with open_write_cursor() as cur:
        add_trigger_query = """INSERT INTO casev3.fulfilment_next_trigger (id, trigger_date_time) VALUES(%s,%s)"""
        trigger_vars = (str(uuid.uuid4()), datetime.utcnow())
        cur.execute(add_trigger_query, vars=trigger_vars)
