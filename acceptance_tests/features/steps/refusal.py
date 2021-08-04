import json

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
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
                        "caseId": context.emitted_cases[0]['caseId'],
                    }
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_REFUSAL_TOPIC)
