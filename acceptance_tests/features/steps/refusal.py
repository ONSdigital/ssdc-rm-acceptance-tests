import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a REFUSAL event is received")
def send_refusal_msg(context):
    message = json.dumps(
        {
            "header": {
                "topic": Config.PUBSUB_REFUSAL_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4()),
                "originatingUser": "foo@bar.com"
            },
            "payload": {
                "refusal": {
                    "caseId": context.emitted_cases[0]['caseId'],
                    "type": "EXTRAORDINARY_REFUSAL"
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_REFUSAL_TOPIC)
