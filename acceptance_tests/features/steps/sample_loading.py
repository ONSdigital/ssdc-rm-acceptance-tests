import json
from pathlib import Path
import time

from behave import *
from sample_loader.load_sample import load_sample_file

from acceptance_tests.utilities.database_helper import add_survey_and_collex_to_db, poll_database_with_timeout
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

RESOURCE_FILE_PATH = Path(__file__).parents[3].joinpath('resources')

use_step_matcher("re")


@given("sample file is loaded successfully")
# @step('sample file "sample_file_name" is loaded successfully')
def load_sample_file_successfully_step(context):
    load_sample_file_helper(context, "sample_1_english_HH_unit.csv")

    # get_and_check_sample_load_case_created_messages(context)
    # get_and_check_uac_updated_messages(context)

    poll_until_sample_is_ingested(context)



def load_sample_file_helper(context, sample_file_name):
    sample_units_raw = _load_sample(context, sample_file_name)
    context.sample_count = len(sample_units_raw)

    context.sample_units = [
        json.loads(sample_unit)
        for sample_unit in sample_units_raw.values()
    ]


def _load_sample(context, sample_file_name):
    sample_file_path = RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
    add_survey_and_collex_to_db(context)
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
