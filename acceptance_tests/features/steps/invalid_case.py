import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step('an INVALID_CASE event is received')
def send_invalid_case(context):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_invalid_case_message(context.correlation_id, context.originating_user,
                                         context.emitted_cases[0]['caseId'])
    context.sent_messages.append(message)


@step('a bad invalid case message is put on the topic')
def a_bad_invalid_case_message_is_put_on_the_topic(context):
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_invalid_case_message(str(uuid.uuid4()), context.originating_user,
                                         "7abb3c15-e850-4a9f-a0c2-6749687915a8")
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.sent_messages.append(message)


def _send_invalid_case_message(correlation_id, originating_user, case_id):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_INVALID_CASE_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": correlation_id,
                "originatingUser": originating_user
            },
            "payload": {
                "invalidCase": {
                    "reason": "Business has gone bankrupt",
                    "caseId": case_id
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_INVALID_CASE_TOPIC)

    return message
