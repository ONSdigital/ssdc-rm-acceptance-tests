import json

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("an INVALID_CASE event is received")
def send_invalid_case_msg(context):
    message = json.dumps(
        {
            "event": {
                "type": "INVALID_CASE",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2021-06-09T13:49:19.716761Z",
                "transactionId": "92df974c-f03e-4519-8d55-05e9c0ecea43"
            },
            "payload": {
                "invalidCase": {
                    "reason": "Business has gone bankrupt",
                    "caseId": context.emitted_cases[0]['caseId']
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_INVALID_CASE_TOPIC)
