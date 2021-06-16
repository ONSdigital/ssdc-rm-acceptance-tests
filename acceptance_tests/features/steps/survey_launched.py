import json

from behave import step

from acceptance_tests.utilities.rabbit_context import RabbitContext
from config import Config


@step("a survey launched msg is put on the queue")
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
                    "questionnaireId": context.uac_created_events['questionnaireId'],
                    "agentId": "cc_000351"
                }
            }
        }
    )

    with RabbitContext(exchange=Config.RABBITMQ_EVENT_EXCHANGE) as rabbit:
        rabbit.publish_message(
            message=message,
            content_type='application/json',
            routing_key=Config.RABBITMQ_SURVEY_LAUNCHED_ROUTING_KEY)
