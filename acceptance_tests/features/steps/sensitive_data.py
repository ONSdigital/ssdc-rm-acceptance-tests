import json

from behave import step
from tenacity import retry, wait_fixed, stop_after_delay

from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.rabbit_helper import publish_json_message
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("an UPDATE_SAMPLE_SENSITIVE event is received updating the {sensitive_column} to {new_value}")
def send_update_sample_sensitive_msg(context, sensitive_column, new_value):
    message = json.dumps(
        {
            "event": {
                "type": "UPDATE_SAMPLE_SENSITIVE",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2021-06-09T13:49:19.716761Z",
                "transactionId": "92df974c-f03e-4519-8d55-05e9c0ecea43"
            },
            "payload": {
                "updateSampleSensitive": {
                    "caseId": context.emitted_cases[0]['caseId'],
                    "sampleSensitive": {sensitive_column: new_value}
                }
            }
        })

    publish_json_message(message, exchange=Config.RABBITMQ_EVENT_EXCHANGE,
                         routing_key=Config.RABBITMQ_UPDATE_SAMPLE_SENSITIVE_ROUTING_KEY)


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
