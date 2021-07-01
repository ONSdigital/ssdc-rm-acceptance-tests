from pathlib import Path

import requests
from behave import step
from requests_toolbelt import MultipartEncoder

from acceptance_tests.features.steps.message_listener import get_emitted_cases
from acceptance_tests.utilities.collex_and_survey_helper import add_survey_and_collex
from acceptance_tests.utilities.test_case_helper import test_helper
from acceptance_tests.utilities.validation_rule_helper import get_sample_rows_and_validation_rules
from config import Config

RESOURCE_FILE_PATH = Path(__file__).parents[3].joinpath('resources')


def get_emitted_cases_and_check_against_sample(context, type_filter, sample_rows):
    emitted_cases = get_emitted_cases(context, type_filter, len(sample_rows))

    for emitted_case in emitted_cases:
        matched_row = None
        for sample_row in sample_rows:

            if sample_row == emitted_case['sample']:
                matched_row = sample_row
                break

        if matched_row:
            sample_rows.remove(matched_row)
        else:
            test_helper.fail(f"Could not find matching row in the sample data for case: {emitted_case}")

    return emitted_cases


@step('sample file "{sample_file_name}" is loaded successfully')
def load_sample_file_step(context, sample_file_name):
    sample_file_path = RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
    sample_rows, validation_rules = get_sample_rows_and_validation_rules(sample_file_path)

    add_survey_and_collex(context, validation_rules)

    upload_file_via_support_tool(context, sample_file_path)

    context.emitted_cases = get_emitted_cases_and_check_against_sample(context, 'CASE_CREATED', sample_rows)

    context.emitted_cases_id = [emitted_case['caseId'] for emitted_case in context.emitted_cases]


def upload_file_via_support_tool(context, sample_file_path):
    multipart_data = MultipartEncoder(fields={
        'collectionExerciseId': context.collex_id,
        'file': ('sample_file', open(sample_file_path, 'rb'), 'text/plain')
    })
    url = f'{Config.SUPPORT_TOOL}/upload'

    response = requests.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    response.raise_for_status()
