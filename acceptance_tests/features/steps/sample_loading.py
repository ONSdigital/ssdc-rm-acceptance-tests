from behave import *
import json
from pathlib import Path

from sample_loader.load_sample import load_sample_file

from config import Config

RESOURCE_FILE_PATH = Path(__file__).parents[1].joinpath('resources')

use_step_matcher("re")

@given("sample file is loaded successfully")
# @step('sample file "sample_file_name" is loaded successfully')
def load_sample_file_successfully_step(context):
    load_sample_file_helper(context, "sample_1_english_HH_unit.csv")

    # get_and_check_sample_load_case_created_messages(context)
    # get_and_check_uac_updated_messages(context)

    # poll_until_sample_is_ingested_to_action(context)


def load_sample_file_helper(context, sample_file_name):
    sample_units_raw = _load_sample(context, sample_file_name)
    context.sample_count = len(sample_units_raw)

    context.sample_units = [
        json.loads(sample_unit)
        for sample_unit in sample_units_raw.values()
    ]


def _load_sample(context, sample_file_name):
    sample_file_path = RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
    return load_sample_file(sample_file_path, context.collection_exercise_id, context.action_plan_id,
                            store_loaded_sample_units=True,
                            host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT,
                            vhost=Config.RABBITMQ_VHOST, exchange=Config.RABBITMQ_EXCHANGE,
                            user=Config.RABBITMQ_USER, password=Config.RABBITMQ_PASSWORD,
                            queue_name=Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)


# def poll_until_sample_is_ingested_to_action(context, after_date_time=None):
#     if not after_date_time:
#         after_date_time = context.test_start_utc
#     query = "SELECT count(*) FROM actionv2.cases WHERE action_plan_id = %s AND created_date_time > %s"
#
#     def success_callback(db_result, timeout_deadline):
#         if db_result[0][0] == context.sample_count:
#             return True
#         elif time.time() > timeout_deadline:
#             test_helper.fail(
#                 f"For Action-plan {context.action_plan_id}, DB didn't have the expected number of sample units. "
#                 f"Expected: {context.sample_count}, actual: {db_result[0][0]}")
#         return False
#
#     poll_action_database_with_timeout(query, (context.action_plan_id, after_date_time),
#                                       success_callback)
