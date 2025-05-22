import csv
import hashlib
import json
import random
import uuid
from datetime import datetime, timezone
from behave import step
from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.file_to_process_upload_helper import upload_and_process_file_by_api
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step('a refusal event is received and erase data is "{erase_data}"')
def send_refusal(context, erase_data):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_refusal_message(context.correlation_id, context.originating_user,
                                    context.emitted_cases[0]['caseId'], erase_data)
    context.sent_messages.append(message)


@step('a bad refusal event is put on the topic')
def send_bad_refusal_message(context):
    context.originating_user = add_random_suffix_to_email(context.scenario_name)
    message = _send_refusal_message(str(uuid.uuid4()), context.originating_user,
                                    "1c1e495d-8f49-4d4c-8318-6174454eb605")
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]
    context.sent_messages.append(message)


def _send_refusal_message(correlation_id, originating_user, case_id, erase_data=False):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_REFUSAL_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": correlation_id,
                "originatingUser": originating_user
            },
            "payload": {
                "refusal": {
                    "caseId": case_id,
                    "type": "EXTRAORDINARY_REFUSAL",
                    "eraseData": erase_data
                }
            }
        })

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_REFUSAL_TOPIC)

    return message


@step('a bulk refusal file is created for every case created and uploaded')
def create_and_upload_bulk_refusal_file(context):
    bulk_refusals_file = f'/tmp/bulk_refusal_{str(uuid.uuid4())}.csv'
    context.bulk_refusals = {}

    for emitted_case in context.emitted_cases:
        caseId = emitted_case['caseId']

        context.bulk_refusals[caseId] = random.choice(
            ('HARD_REFUSAL',
             'EXTRAORDINARY_REFUSAL')
        )

    test_helper.assertGreater(len(context.bulk_refusals), 0, 'Must have at least one refusal for this test to be valid')

    with open(bulk_refusals_file, 'w') as bulk_refusal_file_write:
        writer = csv.DictWriter(bulk_refusal_file_write, fieldnames=['caseId', 'refusalType'])
        writer.writeheader()
        for case_id, refusal_type in context.bulk_refusals.items():
            writer.writerow({'caseId': case_id, 'refusalType': refusal_type})

    upload_and_process_file_by_api(context.collex_id, bulk_refusals_file, 'BULK_REFUSAL')
