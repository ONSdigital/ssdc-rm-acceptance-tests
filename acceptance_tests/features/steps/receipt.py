import json

from behave import step

from acceptance_tests.utilities.rabbit_context import RabbitContext
from config import Config


@step("a case receipt msg is put on the queue")
def receipting_case(context):
    message = json.dumps(
        {
            "event": {
                "type": "RESPONSE_RECEIVED",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2021-06-09T14:10:11.910719Z",
                "transactionId": "730af73e-398d-41d2-893a-cd0722151f9c"
            },
            "payload": {
                "response": {
                    "questionnaireId": context.uac_created_events[0]['payload']['uac']['questionnaireId'],
                    "dateTime": "2019-07-07T22:37:11.988+0000"
                }
            }
        })

    with RabbitContext(exchange='') as rabbit:
        rabbit.publish_message(
            message=message,
            content_type='application/json',
            routing_key=Config.RABBITMQ_RESPONSE_QUEUE)


@step("the receipt msg is put on the GCP pubsub")
def send_receipt(context):
    _publish_object_finalize(context, questionnaire_id=context.qid_to_receipt)
    test_helper.assertTrue(context.sent_to_gcp)
