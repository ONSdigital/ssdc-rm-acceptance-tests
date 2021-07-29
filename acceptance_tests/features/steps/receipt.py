import json
import uuid

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a receipt message is published to the pubsub receipting topic")
def send_receipt(context):
    message = json.dumps({
        "event": {
            "type": "RESPONSE_RECEIVED",
            "source": "RH",
            "channel": "RH",
            "dateTime": "2021-06-09T14:10:11.910719Z",
            "transactionId": str(uuid.uuid4())
        },
        "payload": {
            "response": {
                "questionnaireId": context.emitted_uacs[0]['questionnaireId'],
                "dateTime": "2021-06-09T14:10:11.909472Z"
            }
        }
    })

    publish_to_pubsub(message,
                      Config.RECEIPT_TOPIC_PROJECT,
                      Config.RECEIPT_TOPIC_ID,
                      eventType='OBJECT_FINALIZE')
