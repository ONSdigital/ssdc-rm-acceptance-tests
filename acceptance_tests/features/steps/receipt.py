import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a receipt message is published to the pubsub receipting topic with email address {email_address}")
def send_receipt(context, email_address):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(email_address)
    message = _send_receipt_message(context.correlation_id, context.originating_user, context.emitted_uacs[0]['qid'])
    context.sent_messages.append(message)


@step('a bad receipt message is put on the topic with email address "{email_address}"')
def a_bad_receipt_message_is_put_on_the_topic(context, email_address):
    message = _send_receipt_message(str(uuid.uuid4()), add_random_suffix_to_email(email_address), "987654321")
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.sent_messages.append(message)


def _send_receipt_message(correlation_id, originating_user, qid):
    message = json.dumps({
        "header": {
            "version": Config.EVENT_SCHEMA_VERSION,
            "topic": Config.PUBSUB_RECEIPT_TOPIC,
            "source": "RH",
            "channel": "RH",
            "dateTime": f'{datetime.utcnow().isoformat()}Z',
            "messageId": str(uuid.uuid4()),
            "correlationId": correlation_id,
            "originatingUser": originating_user
        },
        "payload": {
            "receipt": {
                "qid": qid
            }
        }
    })

    publish_to_pubsub(message,
                      Config.PUBSUB_PROJECT,
                      Config.PUBSUB_RECEIPT_TOPIC)

    return message
