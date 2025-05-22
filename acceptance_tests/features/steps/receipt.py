import hashlib
import json
import uuid
from datetime import datetime, timezone

from behave import step

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a receipt message is published to the pubsub receipting topic")
def send_receipt(context):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_receipt_message(context.correlation_id, context.originating_user, context.emitted_uacs[0]['qid'])
    context.sent_messages.append(message)


@step("a receipt message is published to the sdx pubsub receipting topic")
def send_sdx_receipt(context):
    # For the SDX receipt we do not set the correlation id so we need to make sure it's not set for any future checks
    context.correlation_id = None
    message = _send_sdx_receipt(context.emitted_uacs[0]['qid'])
    context.sent_messages.append(message)


@step('a bad receipt message is put on the topic')
def a_bad_receipt_message_is_put_on_the_topic(context):
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_receipt_message(str(uuid.uuid4()), context.originating_user, "987654321")
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.sent_messages.append(message)


def _send_sdx_receipt(qid):
    message = json.dumps({
        "data": {
            "qid": qid,
            "source": "SRM"
        }}
    )

    publish_to_pubsub(message,
                      Config.PUBSUB_PROJECT,
                      'sdx_receipt', content_type="application/json")
    return message


def _send_receipt_message(correlation_id, originating_user, qid):
    message = json.dumps({
        "header": {
            "version": Config.EVENT_SCHEMA_VERSION,
            "topic": Config.PUBSUB_RECEIPT_TOPIC,
            "source": "RH",
            "channel": "RH",
            "dateTime": f'{datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}Z',
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
