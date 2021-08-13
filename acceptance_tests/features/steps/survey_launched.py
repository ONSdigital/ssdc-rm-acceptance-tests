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
                "topic": Config.PUBSUB_SURVEY_LAUNCH_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4()),
                "originatingUser": "foo@bar.com"
            },
            "payload": {
                "surveyLaunch": {
                    "qid": context.emitted_uacs[0]['qid']
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_SURVEY_LAUNCH_TOPIC)
