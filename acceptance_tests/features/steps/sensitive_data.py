import hashlib
import json
import uuid
from datetime import datetime

from behave import step
from tenacity import retry, wait_fixed, stop_after_delay

from acceptance_tests.utilities.audit_trail_helper import get_unique_user_email
from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("an UPDATE_SAMPLE_SENSITIVE event is received updating the {sensitive_column} to {new_value}")
def send_update_sample_sensitive_msg(context, sensitive_column, new_value):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = get_unique_user_email()

    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": context.correlation_id,
                "originatingUser": context.originating_user
            },
            "payload": {
                "updateSampleSensitive": {
                    "caseId": context.emitted_cases[0]['caseId'],
                    "sampleSensitive": {sensitive_column: new_value}
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC)


@step("the {sensitive_column} in the sensitive data on the case has been updated to {expected_value}")
def sensitive_data_on_case_changed(context, sensitive_column, expected_value):
    retry_check_sensitive_data_change(context, sensitive_column, expected_value)


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def retry_check_sensitive_data_change(context, sensitive_column, expected_value):
    with open_cursor() as cur:
        cur.execute("SELECT sample_sensitive FROM casev3.cases WHERE id = %s", (context.emitted_cases[0]['caseId'],))
        result = cur.fetchone()

        test_helper.assertEqual(result[0][sensitive_column], expected_value,
                                f"The {sensitive_column} should have been updated, but it hasn't been")


@step("a bad sensitive data event is put on the topic")
def a_bad_sensitive_data_event_is_put_on_the_topic(context):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": str(uuid.uuid4()),
                "originatingUser": "foo@bar.com"
            },
            "payload": {
                "updateSampleSensitive": {
                    "caseId": "386a50b8-6ba0-40f6-bd3c-34333d58be90",
                    "sampleSensitive": {'favouriteColor': 'Blue'}
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC)
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
