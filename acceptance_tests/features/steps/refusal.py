import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a refusal event is received")
def send_refusal(context):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_refusal_message(context.correlation_id, context.originating_user,
                                    context.emitted_cases[0]['caseId'])
    context.sent_messages.append(message)


@step('a bad refusal event is put on the topic')
def send_bad_refusal_message(context):
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_refusal_message(str(uuid.uuid4()), context.originating_user,
                                    "1c1e495d-8f49-4d4c-8318-6174454eb605")
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.sent_messages.append(message)


def _send_refusal_message(correlation_id, originating_user, case_id):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_REFUSAL_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": correlation_id,
                "originatingUser": originating_user
            },
            "payload": {
                "refusal": {
                    "caseId": case_id,
                    "type": "EXTRAORDINARY_REFUSAL"
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_REFUSAL_TOPIC)

    return message
