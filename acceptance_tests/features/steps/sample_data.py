import csv
import hashlib
import json
import random
import string
import uuid
from datetime import datetime, timezone

from behave import step
from tenacity import retry, stop_after_delay, wait_fixed

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.file_to_process_upload_helper import upload_and_process_file_by_api
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("the {column} in the data on the case has been updated to {expected_value}")
def data_on_case_changed(context, column, expected_value):
    retry_check_data_change(context, column, expected_value)


@step('an UPDATE_SAMPLE event is received updating the {column} to {new_value}')
def send_update_sample(context, column, new_value):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    context.case_id = context.emitted_cases[0]['caseId']
    message = _send_update_sample_msg(context.correlation_id, context.originating_user,
                                      context.case_id, {column: new_value})
    context.sent_messages.append(message)


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def retry_check_data_change(context, column, expected_value):
    with open_cursor() as cur:
        cur.execute("SELECT sample FROM casev3.cases WHERE id = %s", (context.emitted_cases[0]['caseId'],))
        result = cur.fetchone()

        test_helper.assertEqual(result[0][column], expected_value,
                                f"The {column} should have been updated, but it hasn't been")


@step("a bad update sample event is put on the topic")
def a_bad_sample_data_event_is_put_on_the_topic(context):
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_update_sample_msg(str(uuid.uuid4()), context.originating_user,
                                      "386a50b8-6ba0-40f6-bd3c-34333d58be90", {'favouriteColor': 'Blue'})
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.sent_messages.append(message)


def _send_update_sample_msg(correlation_id, originating_user, case_id, update_json):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_UPDATE_SAMPLE_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": correlation_id,
                "originatingUser": originating_user
            },
            "payload": {
                "updateSample": {
                    "caseId": case_id,
                    "sample": update_json
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_UPDATE_SAMPLE_TOPIC)
    return message


@step("a bulk sample update file is created for every case created and uploaded")
def create_and_upload_sample_update_file(context):
    bulk_sample_update_filename = f'/tmp/bulk_sample_update_{str(uuid.uuid4())}.csv'
    context.bulk_sample_update = []

    for emitted_case in context.emitted_cases:
        field_to_update = random.choice(
            ('schoolId',
             'schoolName')
        )

        context.bulk_sample_update.append({
            'caseId': emitted_case['caseId'],
            'fieldToUpdate': field_to_update,
            'newValue': ''.join(random.sample(string.ascii_lowercase, 10))
        })

    test_helper.assertGreater(len(context.bulk_sample_update), 0,
                              'Must have at least one sample update case for this test to be valid')

    with open(bulk_sample_update_filename, 'w') as bulk_file_name_write:
        writer = csv.DictWriter(bulk_file_name_write, fieldnames=['caseId', 'fieldToUpdate', 'newValue'])
        writer.writeheader()
        for case_row in context.bulk_sample_update:
            writer.writerow({'caseId': case_row['caseId'], 'fieldToUpdate': case_row['fieldToUpdate'],
                             'newValue': case_row['newValue']})

    upload_and_process_file_by_api(context.collex_id, bulk_sample_update_filename, job_type='BULK_UPDATE_SAMPLE',
                                   delete_after_upload=True)
