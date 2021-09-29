import json
import uuid

from behave import step

from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step("a newCase event is built and submitted")
def build_new_case_and_submit(context):
    context.case_id = str(uuid.uuid4())
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_NEW_CASE_TOPIC,
                "source": "cupidatat",
                "channel": "EQ",
                "dateTime": "1970-01-01T00:00:00.000Z",
                "messageId": context.case_id,
                "correlationId": context.case_id,
                "originatingUser": "foo.bar@ons.gov.uk"
            },
            "payload": {
                "newCase": {
                    "caseId": context.case_id,
                    "collectionExerciseId": context.collex_id,
                    "sample": {
                        "schoolId": "abc123",
                        "schoolName": "Chesterthorps High School",
                        "consentGivenTest": "true",
                        "consentGivenSurvey": "true"
                    },
                    "sampleSensitive": {
                        "firstName": "Fred",
                        "lastName": "Bloggs",
                        "childFirstName": "Jo",
                        "childMiddleNames": "Rose May",
                        "childLastName": "Pinker",
                        "childDob": "2001-12-31",
                        "additionalInfo": "Class 2A",
                        "childMobileNumber": "07123456789",
                        "childEmailAddress": "jo.rose.may.pinker@domain.com",
                        "parentMobileNumber": "07123456789",
                        "parentEmailAddress": "fred.bloggs@domain.com"
                    }
                }
            }
        }
    )
    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_NEW_CASE_TOPIC)
