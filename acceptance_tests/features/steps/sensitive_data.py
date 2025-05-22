import csv
import hashlib
import json
import random
import string
import uuid
from datetime import datetime, timezone

from behave import step
from tenacity import retry, wait_fixed, stop_after_delay

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.event_helper import get_emitted_cases
from acceptance_tests.utilities.file_to_process_upload_helper import upload_and_process_file_by_api
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("the {sensitive_column} in the sensitive data on the case has been updated to {expected_value}")
def sensitive_data_on_case_changed(context, sensitive_column, expected_value):
    retry_check_sensitive_data_change(context.case_id, sensitive_column, expected_value)


@step(
    'an UPDATE_SAMPLE_SENSITIVE event is received updating the {sensitive_column} to {new_value}')
def send_update_sample_sensitive(context, sensitive_column, new_value):
    context.correlation_id = str(uuid.uuid4())
    context.case_id = context.emitted_cases[0]['caseId']
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_update_sample_sensitive_msg(context.correlation_id, context.originating_user,
                                                context.case_id, {sensitive_column: new_value})
    context.sent_messages.append(message)


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def retry_check_sensitive_data_change(case_id, sensitive_column, expected_value):
    with open_cursor() as cur:
        cur.execute("SELECT sample_sensitive FROM casev3.cases WHERE id = %s", (case_id,))
        result = cur.fetchone()

        test_helper.assertEqual(result[0][sensitive_column], expected_value,
                                f"The {sensitive_column} should have been updated, but it hasn't been")

        return result[0]


@step("a bad update sample sensitive event is put on the topic")
def a_bad_sensitive_data_event_is_put_on_the_topic(context):
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_update_sample_sensitive_msg(str(uuid.uuid4()), context.originating_user,
                                                "386a50b8-6ba0-40f6-bd3c-34333d58be90", {'favouriteColor': 'Blue'})
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.sent_messages.append(message)


def _send_update_sample_sensitive_msg(correlation_id, originating_user, case_id, update_json):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": correlation_id,
                "originatingUser": originating_user
            },
            "payload": {
                "updateSampleSensitive": {
                    "caseId": case_id,
                    "sampleSensitive": update_json
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_UPDATE_SAMPLE_SENSITIVE_TOPIC)
    return message


@step("a bulk sensitive update file is created for every case created and uploaded")
def create_and_upload_sensitive_update_file(context):
    bulk_sensitive_update_filename = f'/tmp/bulk_sensitive_update_{str(uuid.uuid4())}.csv'
    context.bulk_sensitive_update = []

    for emitted_case in context.emitted_cases:
        field_to_update = random.choice(
            ('firstName',
             'lastName',
             'childFirstName',
             'childMiddleNames',
             'childLastName')
        )

        context.bulk_sensitive_update.append({
            'caseId': emitted_case['caseId'],
            'fieldToUpdate': field_to_update,
            'newValue': ''.join(random.sample(string.ascii_lowercase, 26))
        })

    test_helper.assertGreater(len(context.bulk_sensitive_update), 0,
                              'Must have at least one sample update case for this test to be valid')

    with open(bulk_sensitive_update_filename, 'w') as bulk_file_name_write:
        writer = csv.DictWriter(bulk_file_name_write, fieldnames=['caseId', 'fieldToUpdate', 'newValue'])
        writer.writeheader()
        for case_row in context.bulk_sensitive_update:
            writer.writerow({'caseId': case_row['caseId'], 'fieldToUpdate': case_row['fieldToUpdate'],
                             'newValue': case_row['newValue']})

    upload_and_process_file_by_api(context.collex_id, bulk_sensitive_update_filename,
                                   job_type='BULK_UPDATE_SAMPLE_SENSITIVE',
                                   delete_after_upload=True)


@step("in the database the sensitive data has been updated as expected and is emitted redacted")
def sensitive_data_updated_in_database_as_expected_and_is_emitted(context):
    emitted_updated_cases = get_emitted_cases(len(context.bulk_sensitive_update), context.test_start_utc_datetime)

    for expected_update in context.bulk_sensitive_update:
        db_sample_sensitive_dict = retry_check_sensitive_data_change(expected_update['caseId'],
                                                                     expected_update['fieldToUpdate'],
                                                                     expected_update['newValue'])
        emitted_sample_sensitive = get_emitted_case_by_id(expected_update['caseId'], emitted_updated_cases)[
            'sampleSensitive']

        test_helper.assertEqual(len(db_sample_sensitive_dict), len(emitted_sample_sensitive),
                                'Expected emitted and DB sensitive columns to be the same length')

        for column_name, db_value in db_sample_sensitive_dict.items():
            test_helper.assertIn(column_name, emitted_sample_sensitive.keys(),
                                 f'Failed to find expected column {column_name}'
                                 f' in emitted case sample sensitive {emitted_sample_sensitive}')

            if db_value:
                expected_value = 'REDACTED'
            else:
                expected_value = ''

            test_helper.assertEqual(emitted_sample_sensitive[column_name], expected_value,
                                    f'Emitted case update value of {emitted_sample_sensitive[column_name]} '
                                    f'did not match expected value [{expected_value}]')


def get_emitted_case_by_id(case_id_to_match, all_emitted_update_cases):
    for updated_case in all_emitted_update_cases:
        if updated_case['caseId'] == case_id_to_match:
            return updated_case

    test_helper.fail(f"Couldn't find case update emitted with case ID: {case_id_to_match}"
                     f" Full emitted_case_update_events list: {all_emitted_update_cases}")
