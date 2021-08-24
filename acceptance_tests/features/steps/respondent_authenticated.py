import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a UAC_AUTHENTICATION event is received")
def send_respondent_authenticated_msg(context):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_UAC_AUTHENTICATION_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4())
            },
            "payload": {
                "uacAuthentication": {
                    "qid": context.emitted_uacs[0]['qid']
                }
            }
        }
    )
    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_UAC_AUTHENTICATION_TOPIC)


@step("a bad respondent authenticated event is out on the topic")
def a_bad_respondent_authenticated_event_is_out_on_the_topic(context):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_UAC_AUTHENTICATION_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4())
            },
            "payload": {
                "uacAuthentication": {
                    "qid": "666"
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_UAC_AUTHENTICATION_TOPIC)
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
