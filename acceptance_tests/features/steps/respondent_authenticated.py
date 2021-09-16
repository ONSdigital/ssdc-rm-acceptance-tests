import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step('a UAC_AUTHENTICATION event is received with email address "{email_address}"')
def send_respondent_authenticated(context, email_address):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(email_address)
    message = _send_respondent_authenticated_message(context.correlation_id, context.originating_user,
                                                     context.emitted_uacs[0]['qid'])
    context.sent_messages.append(message)


@step('a bad respondent authenticated event is put on the topic with email address "{email_address}"')
def a_bad_respondent_authenticated_event_is_put_on_the_topic(context, email_address):
    message = _send_respondent_authenticated_message(str(uuid.uuid4()),
                                                     add_random_suffix_to_email(email_address),
                                                     "666")
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.sent_messages.append(message)


def _send_respondent_authenticated_message(correlation_id, originating_user, qid):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_UAC_AUTHENTICATION_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": correlation_id,
                "originatingUser": originating_user
            },
            "payload": {
                "uacAuthentication": {
                    "qid": qid
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_UAC_AUTHENTICATION_TOPIC)

    return message
