import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step('a deactivate uac message is put on the queue with email_address "{email_address}"')
def put_deactivate_uac_on_topic(context, email_address):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(email_address)

    message = _send_deactivate_uac_message(context.correlation_id, context.originating_user,
                                           context.emitted_uacs[0]['qid'])
    context.sent_messages.append(message)


@step('a bad deactivate uac message is put on the topic with email address "{email_address}"')
def a_bad_deactivate_uac_message_is_put_on_the_topic(context, email_address):
    message = _send_deactivate_uac_message(str(uuid.uuid4()), add_random_suffix_to_email(email_address), "123456789")
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]


def _send_deactivate_uac_message(correlation_id, originating_user, qid):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_DEACTIVATE_UAC_TOPIC,
                "source": "CC",
                "channel": "CC",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": correlation_id,
                "originatingUser": originating_user
            },
            "payload": {
                "deactivateUac": {
                    "qid": qid,
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_DEACTIVATE_UAC_TOPIC)

    return message
