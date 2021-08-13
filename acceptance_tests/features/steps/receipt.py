import json
import uuid

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a receipt message is published to the pubsub receipting topic")
def send_receipt(context):
    message = json.dumps({
        "event": {
            "type": "RECEIPT",
            "source": "RH",
            "channel": "RH",
            "dateTime": "2021-06-09T14:10:11.910719Z",
            "transactionId": str(uuid.uuid4())
        },
        "payload": {
            "receipt": {
                "qid": context.emitted_uacs[0]['qid']
            }
        }
    })

    publish_to_pubsub(message,
                      Config.PUBSUB_PROJECT,
                      Config.PUBSUB_RECEIPT_TOPIC)
