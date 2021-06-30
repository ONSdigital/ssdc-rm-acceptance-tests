import json
import time
from pathlib import Path

import requests
from behave import step
from requests_toolbelt import MultipartEncoder
from sample_loader.load_sample import load_sample_file

from acceptance_tests.features.steps.message_listener import get_emitted_cases
from acceptance_tests.utilities.collex_and_survey_helper import add_survey_and_collex
from acceptance_tests.utilities.database_helper import poll_database_with_timeout
from acceptance_tests.utilities.test_case_helper import test_helper
from acceptance_tests.utilities.validation_rule_helper import get_sample_rows_and_validation_rules
from config import Config

RESOURCE_FILE_PATH = Path(__file__).parents[3].joinpath('resources')


def get_emitted_cases_and_check_against_sample(context, type_filter, sample_rows):
    loaded_cases = get_emitted_cases(context, type_filter, len(sample_rows))

    for loaded_case in loaded_cases:
        matched_row = None
        for sample_row in sample_rows:

            if sample_row == loaded_case['sample']:
                matched_row = sample_row
                break

        if matched_row:
            sample_rows.remove(matched_row)
        else:
            test_helper.fail(f"Could not find matching row in the sample data for case: {loaded_case}")

    return loaded_cases


@step('sample file "{sample_file_name}" is loaded successfully')
def load_sample_file_step(context, sample_file_name):
    sample_file_path = RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
    sample_rows, validation_rules = get_sample_rows_and_validation_rules(sample_file_path)

    add_survey_and_collex(context, validation_rules)

    upload_file_via_support_tool(context, sample_file_path)

    context.loaded_cases = get_emitted_cases_and_check_against_sample(context, 'CASE_CREATED', sample_rows)

    context.loaded_case_ids = [loaded_case['caseId'] for loaded_case in context.loaded_cases]


def upload_file_via_support_tool(context, sample_file_path):
    multipart_data = MultipartEncoder(fields={
        'collectionExerciseId': context.collex_id,
        'file': ('sample_file', open(sample_file_path, 'rb'), 'text/plain')
    })
    url = f'{Config.SUPPORT_TOOL}/upload'

    response = requests.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    response.raise_for_status()


def load_sample_file_helper(context, sample_file_name):
    sample_units_raw = _load_sample(context, sample_file_name)
    context.sample_count = len(sample_units_raw)

    context.sample_units = [
        json.loads(sample_unit)
        for sample_unit in sample_units_raw
    ]


def _load_sample(context, sample_file_name):
    sample_file_path = RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
    return load_sample_file(sample_file_path, context.collex_id,
                            store_loaded_sample_units=True,
                            host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT,
                            vhost=Config.RABBITMQ_VHOST, exchange=Config.RABBITMQ_EXCHANGE,
                            user=Config.RABBITMQ_USER, password=Config.RABBITMQ_PASSWORD,
                            queue_name=Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)


def poll_until_sample_is_ingested(context, after_date_time=None):
    if not after_date_time:
        after_date_time = context.test_start_utc
    query = "SELECT count(*) FROM casev3.cases WHERE collection_exercise_id = %s AND created_at > %s"

    def success_callback(db_result, timeout_deadline):
        if db_result[0][0] == context.sample_count:
            return True
        elif time.time() > timeout_deadline:
            test_helper.fail(
                f"For collection exercise {context.collex_id}, DB didn't have the expected number of sample units. "
                f"Expected: {context.sample_count}, actual: {db_result[0][0]}")
        return False

    poll_database_with_timeout(query, (context.collex_id, after_date_time),
                               success_callback)
