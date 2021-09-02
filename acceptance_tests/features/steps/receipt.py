import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import get_unique_user_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a receipt message is published to the pubsub receipting topic")
def send_receipt(context):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = get_unique_user_email()

    message = json.dumps({
        "header": {
            "version": Config.EVENT_SCHEMA_VERSION,
            "topic": Config.PUBSUB_RECEIPT_TOPIC,
            "source": "RH",
            "channel": "RH",
            "dateTime": f'{datetime.utcnow().isoformat()}Z',
            "messageId": str(uuid.uuid4()),
            "correlationId": context.correlation_id,
            "originatingUser": context.originating_user
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


@step("a bad receipt message is put on the topic")
def a_bad_receipt_message_is_put_on_the_topic(context):
    message = json.dumps({
        "header": {
            "version": Config.EVENT_SCHEMA_VERSION,
            "topic": Config.PUBSUB_RECEIPT_TOPIC,
            "source": "RH",
            "channel": "RH",
            "dateTime": f'{datetime.utcnow().isoformat()}Z',
            "messageId": str(uuid.uuid4()),
            "correlationId": str(uuid.uuid4()),
            "originatingUser": "foo@bar.com"
        },
        "payload": {
            "receipt": {
                "qid": "987654321"
            }
        }
    })

    publish_to_pubsub(message,
                      Config.PUBSUB_PROJECT,
                      Config.PUBSUB_RECEIPT_TOPIC)
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
