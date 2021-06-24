import json

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("the receipt msg is put on the GCP pubsub")
def send_receipt(context):
    _publish_object_finalize(context,
                             questionnaire_id=context.uac_created_events[0]['payload']['uac']['questionnaireId'])
    test_helper.assertTrue(context.sent_to_gcp)


def _publish_object_finalize(context, case_id="0", tx_id="3d14675d-a25d-4672-a0fe-b960586653e8", questionnaire_id="0"):
    context.sent_to_gcp = False

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

    context.sent_to_gcp = True
