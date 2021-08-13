import json

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a SURVEY_LAUNCH event is received")
def send_survey_launched_msg(context):
    message = json.dumps(
        {
            "event": {
                "type": "SURVEY_LAUNCH",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2011-08-12T20:17:46.384Z",
                "transactionId": "c45de4dc-3c3b-11e9-b210-d663bd873d93"
            },
            "payload": {
                "surveyLaunch": {
                    "qid": context.emitted_uacs[0]['qid']
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_SURVEY_LAUNCH_TOPIC)
