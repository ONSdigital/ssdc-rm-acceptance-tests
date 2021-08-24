import hashlib
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
                "version": Config.EVENT_SCHEMA_VERSION,
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


@step("a bad REFUSAL event is put on the topic")
def step_impl(context):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
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
                    "caseId": "1c1e495d-8f49-4d4c-8318-6174454eb605",
                    "type": "EXTRAORDINARY_REFUSAL"
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_REFUSAL_TOPIC)
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.subscriptions_to_purge = [Config.PUBSUB_REFUSAL_RM_SUBSCRIPTION]
