import json

from behave import step

from acceptance_tests.utilities.rabbit_context import RabbitContext
from config import Config


@step("a invalid address msg is put on the queue")
def send_invalid_address_msg(context):
    message = json.dumps(
        {
            "event": {
                "type": "ADDRESS_NOT_VALID",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2021-06-09T13:49:19.716761Z",
                "transactionId": "92df974c-f03e-4519-8d55-05e9c0ecea43"
            },
            "payload": {
                "invalidAddress": {
                    "reason": "Not found",
                    "notes": "Looked hard",
                    "caseId": context.emitted_cases_id[0]
                }
            }
        })

    with RabbitContext(exchange='') as rabbit:
        rabbit.publish_message(
            message=message,
            content_type='application/json',
            routing_key=Config.RABBITMQ_INVALID_ADDRESS_QUEUE)
