import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a SURVEY_LAUNCH event is received")
def send_survey_launched_msg(context):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_SURVEY_LAUNCH_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4())
            },
            "payload": {
                "surveyLaunch": {
                    "qid": context.emitted_uacs[0]['qid']
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_SURVEY_LAUNCH_TOPIC)


@step("a bad survey launched event is put on the topic")
def step_impl(context):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_SURVEY_LAUNCH_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4())
            },
            "payload": {
                "surveyLaunch": {
                    "qid": "555555"
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_SURVEY_LAUNCH_TOPIC)
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
