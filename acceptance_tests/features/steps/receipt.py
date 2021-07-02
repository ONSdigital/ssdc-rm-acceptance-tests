import json

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a receipt message is published to the pubsub receipting topic")
def send_receipt(context):
    _publish_object_finalize(questionnaire_id=context.emitted_uacs[0]['questionnaireId'])


def _publish_object_finalize(case_id="0", tx_id="3d14675d-a25d-4672-a0fe-b960586653e8", questionnaire_id="0"):
    data = json.dumps({
        "timeCreated": "2008-08-24T00:00:00Z",
        "metadata": {
            "case_id": case_id,
            "tx_id": tx_id,
            "questionnaire_id": questionnaire_id,
        }
    })

    publish_to_pubsub(data,
                      Config.RECEIPT_TOPIC_PROJECT,
                      Config.RECEIPT_TOPIC_ID,
                      eventType='OBJECT_FINALIZE',
                      bucketId='eq-bucket',
                      objectId=tx_id)
