import requests
from behave import step
from requests_toolbelt import MultipartEncoder

from acceptance_tests.utilities.collex_and_survey_helper import add_collex, add_survey
from acceptance_tests.utilities.event_helper import get_emitted_cases
from acceptance_tests.utilities.test_case_helper import test_helper
from acceptance_tests.utilities.validation_rule_helper import get_sample_rows_and_validation_rules
from config import Config


def get_emitted_cases_and_check_against_sample(sample_rows):
    emitted_cases = get_emitted_cases('CASE_CREATED', len(sample_rows))

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
    sample_file_path = Config.RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_validation_rules(sample_file_path)

    context.survey_id, context.survey_name = add_survey(sample_validation_rules)
    context.collex_id, context.collex_name = add_collex(context.survey_id)

    upload_sample_file(context.collex_id, sample_file_path)

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)
    context.emitted_cases_id = [emitted_case['caseId'] for emitted_case in context.emitted_cases]


def upload_sample_file(collex_id, sample_file_path):
    multipart_data = MultipartEncoder(fields={
        'collectionExerciseId': collex_id,
        'file': ('sample_file', open(sample_file_path, 'rb'), 'text/plain')
    })
    url = f'{Config.SUPPORT_TOOL}/upload'

    response = requests.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    response.raise_for_status()
