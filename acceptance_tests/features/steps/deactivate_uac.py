import json

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a deactivate uac message is put on the queue")
def step_impl(context):
    message = json.dumps(
        {
            "event": {
                "type": "DEACTIVATE_UAC",
                "source": "CC",
                "channel": "CC",
                "dateTime": "2021-06-09T13:49:19.716761Z",
                "transactionId": "92df974c-f03e-4519-8d55-05e9c0ecea43"
            },
            "payload": {
                "deactivateUac": {
                    "qid": context.emitted_uacs[0]['questionnaireId'],
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_DEACTIVATE_UAC_TOPIC)
