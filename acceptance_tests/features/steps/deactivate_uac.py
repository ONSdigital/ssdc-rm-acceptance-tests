import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a deactivate uac message is put on the queue")
def step_impl(context):
    message = json.dumps(
        {
            "header": {
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
                    "qid": context.emitted_uacs[0]['qid'],
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_DEACTIVATE_UAC_TOPIC)
