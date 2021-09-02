import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import get_unique_user_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a deactivate uac message is put on the queue")
def put_deactivate_uac_on_topic(context):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = get_unique_user_email()

    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_DEACTIVATE_UAC_TOPIC,
                "source": "CC",
                "channel": "CC",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": context.correlation_id,
                "originatingUser": context.originating_user
            },
            "payload": {
                "deactivateUac": {
                    "qid": context.emitted_uacs[0]['qid'],
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_DEACTIVATE_UAC_TOPIC)


@step("a bad deactivate uac message is put on the topic")
def a_bad_deactivate_uac_message_is_put_on_the_topic(context):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_DEACTIVATE_UAC_TOPIC,
                "source": "CC",
                "channel": "CC",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4()),
                "originatingUser": "foo@bar.com"
            },
            "payload": {
                "deactivateUac": {
                    "qid": "123456789",
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_DEACTIVATE_UAC_TOPIC)
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
