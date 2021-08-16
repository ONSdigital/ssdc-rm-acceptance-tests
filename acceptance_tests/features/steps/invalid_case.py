import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("an INVALID_CASE event is received")
def send_invalid_case_msg(context):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_INVALID_CASE_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4()),
                "originatingUser": "foo@bar.com"
            },
            "payload": {
                "invalidCase": {
                    "reason": "Business has gone bankrupt",
                    "caseId": context.emitted_cases[0]['caseId']
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_INVALID_CASE_TOPIC)
