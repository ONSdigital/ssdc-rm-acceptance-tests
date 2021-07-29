import json
import uuid

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


def _publish_message():
    data = json.dumps({
        "caseId": str(uuid.uuid4()),
        "collectionExerciseId": '310873ef-ae80-42a3-9d51-1cbce79df2de',
        "sample": {
            "ADDRESS_LINE1": "123 Fake Street",
            "ADDRESS_LINE1": "Fake part of town",
            "ADDRESS_LINE1": "Fake suburb",
            "TOWN_NAME": "Fake town",
            "POSTCODE": "F5 3E"
        },
        "sampleSensitive" : {
            "PHONE_NUMBER": "0123456789"
        }
    })

    publish_to_pubsub(data,
                      Config.RECEIPT_TOPIC_PROJECT,
                      "supportTool.caseProcessor.sample.topic")


if __name__ == '__main__':
    _publish_message()
