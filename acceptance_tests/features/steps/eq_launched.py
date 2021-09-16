import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import get_unique_user_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step('an EQ_LAUNCH event is received with email address "{email_address}"')
def send_eq_launched(context, email_address):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = get_unique_user_email()

    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_EQ_LAUNCH_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": context.correlation_id,
                "originatingUser": context.originating_user
            },
            "payload": {
                "eqLaunch": {
                    "qid": context.emitted_uacs[0]['qid']
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_EQ_LAUNCH_TOPIC)


@step('a bad EQ launched event is put on the topic with email address "{email_address}"')
def step_impl(context, email_address):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_EQ_LAUNCH_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4())
            },
            "payload": {
                "eqLaunch": {
                    "qid": "555555"
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_EQ_LAUNCH_TOPIC)
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
