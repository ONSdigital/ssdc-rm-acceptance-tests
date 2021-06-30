import json

from behave import step

from acceptance_tests.utilities.rabbit_context import RabbitContext
from config import Config


@step("a case refused msg is put on the queue")
def send_refusal_msg(context):
    message = json.dumps(
        {
            "event": {
                "type": "REFUSAL_RECEIVED",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2021-06-09T14:10:11.910719Z",
                "transactionId": "730af73e-398d-41d2-893a-cd0722151f9c"
            },
            "payload": {
                "refusal": {
                    "type": "EXTRAORDINARY_REFUSAL",
                    "collectionCase": {
                        "caseId": context.emitted_case_ids[0],
                    }
                }
            }
        })

    with RabbitContext(exchange='') as rabbit:
        rabbit.publish_message(
            message=message,
            content_type='application/json',
            routing_key=Config.RABBITMQ_REFUSAL_QUEUE)
