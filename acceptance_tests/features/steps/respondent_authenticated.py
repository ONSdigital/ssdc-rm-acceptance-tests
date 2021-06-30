import json

from behave import step

from acceptance_tests.utilities.event_helper import check_if_event_list_is_exact_match
from acceptance_tests.utilities.rabbit_context import RabbitContext
from config import Config


@step("a respondent authenticated msg is put on the queue")
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
                    "questionnaireId": context.uac_created_events[0]['payload']['uac']['questionnaireId'],
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


@step("the events logged for the case the respondent has authenticated against are {expected_event_list}")
def check_survey_launch_event_logging(context, expected_event_list):
    check_if_event_list_is_exact_match(expected_event_list, context.loaded_case_ids[0])
