import json

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a RESPONDENT_AUTHENTICATED event is received")
def send_respondent_authenticated_msg(context):
    message = json.dumps(
        {
            "event": {
                "type": "RESPONDENT_AUTHENTICATED",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2011-08-12T20:17:46.384Z",
                "transactionId": "c45de4dc-3c3b-11e9-b210-d663bd873d93"
            },
            "payload": {
                "response": {
                    "questionnaireId": context.emitted_uacs[0]['questionnaireId'],
                    "agentId": "cc_000351"
                }
            }
        }
    )
    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_SURVEY_LAUNCHED_TOPIC)
