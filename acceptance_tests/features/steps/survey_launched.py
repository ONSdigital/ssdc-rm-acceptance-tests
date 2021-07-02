import json

from behave import step

from acceptance_tests.utilities.rabbit_helper import publish_json_message
from config import Config


@step("a SURVEY_LAUNCHED event is received")
def send_survey_launched_msg(context):
    message = json.dumps(
        {
            "event": {
                "type": "SURVEY_LAUNCHED",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2011-08-12T20:17:46.384Z",
                "transactionId": "c45de4dc-3c3b-11e9-b210-d663bd873d93"
            },
            "payload": {
                "response": {
                    "questionnaireId": context.uac_created_events[0]['payload']['uac']['questionnaireId'],
                    "agentId": "cc_000351"
                }
            }
        }
    )

    publish_json_message(message, exchange=Config.RABBITMQ_EVENT_EXCHANGE,
                         routing_key=Config.RABBITMQ_SURVEY_LAUNCHED_ROUTING_KEY)
