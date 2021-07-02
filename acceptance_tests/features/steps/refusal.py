import json

from behave import step

from acceptance_tests.utilities.rabbit_helper import publish_json_message
from config import Config


@step("a REFUSAL_RECEIVED event is received")
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
                        "caseId": context.emitted_cases_id[0],
                    }
                }
            }
        })

    publish_json_message(message, exchange=Config.RABBITMQ_EVENT_EXCHANGE, routing_key=Config.RABBITMQ_REFUSAL_QUEUE)
