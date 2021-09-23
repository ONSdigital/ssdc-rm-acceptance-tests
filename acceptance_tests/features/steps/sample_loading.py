import csv
import time
from pathlib import Path

import requests
from behave import step
from requests_toolbelt import MultipartEncoder

from acceptance_tests.utilities.collex_helper import add_collex
from acceptance_tests.utilities.event_helper import get_emitted_cases
from acceptance_tests.utilities.survey_helper import add_survey
from acceptance_tests.utilities.test_case_helper import test_helper
from acceptance_tests.utilities.validation_rule_helper import get_sample_rows_and_validation_rules
from config import Config


def get_emitted_cases_and_check_against_sample(sample_rows, sensitive_columns=[]):
    emitted_cases = get_emitted_cases(len(sample_rows))

    for emitted_case in emitted_cases:
        matched_row = None
        for sample_row in sample_rows:

            if equal_dicts(sample_row, emitted_case['sample'], sensitive_columns):
                matched_row = sample_row
                break

        if matched_row:
            sample_rows.remove(matched_row)
        else:
            test_helper.fail(f"Could not find matching row in the sample data for case: {emitted_case} "
                             f"all emitted cases: {emitted_cases}")

    return emitted_cases


def equal_dicts(d1, d2, ignore_keys):
    d1_filtered = {k: v for k, v in d1.items() if k not in ignore_keys}
    d2_filtered = {k: v for k, v in d2.items() if k not in ignore_keys}
    return d1_filtered == d2_filtered


@step('BOM sample file "{sample_file_name}" is loaded successfully')
def load_bom_sample_file_step(context, sample_file_name):
    sample_file_path = Config.RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_validation_rules(sample_file_path)

    # Fix the BOM mess
    sample_validation_rules[0]['columnName'] = 'TLA'
    for index in range(len(sample_rows)):
        sample_rows[index]['TLA'] = sample_rows[index].pop('\ufeffTLA')

    context.survey_id = add_survey(sample_validation_rules)
    context.collex_id = add_collex(context.survey_id)

    upload_sample_file(context.collex_id, sample_file_path)

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


@step('sample file "{sample_file_name}" is loaded successfully')
def load_sample_file_step(context, sample_file_name):
    sample_file_path = Config.RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_validation_rules(sample_file_path)

    context.survey_id = add_survey(sample_validation_rules)
    context.collex_id = add_collex(context.survey_id)

    upload_sample_file(context.collex_id, sample_file_path)

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


def get_business_sample_columns_and_validation_rules(sample_file_path: Path):
    sample_columns = ["ruref",
                      "checkletter",
                      "frosic92",
                      "rusic92",
                      "frosic2007",
                      "rusic2007",
                      "froempment",
                      "frotover",
                      "entref",
                      "legalstatus",
                      "entrepmkr",
                      "region",
                      "birthdate",
                      "entname1",
                      "entname2",
                      "entname3",
                      "runame1",
                      "runame2",
                      "runame3",
                      "tradstyle1",
                      "tradstyle2",
                      "tradstyle3",
                      "seltype",
                      "inclexcl",
                      "cell_no",
                      "formtype",
                      "currency"]

    validation_rules = [{'columnName': column, 'rules': []} for column in sample_columns]

    with open(sample_file_path) as sample_file:
        reader = csv.DictReader(sample_file, fieldnames=sample_columns, delimiter=':')
        sample_rows = [row for row in reader]

    return sample_rows, validation_rules


@step('business sample file is loaded successfully')
def load_business_sample_file_step(context):
    sample_file_path = Config.RESOURCE_FILE_PATH.joinpath('sample_files', 'business_rsi_example_sample.csv')
    sample_rows, validation_rules = get_business_sample_columns_and_validation_rules(sample_file_path)

    context.survey_id = add_survey(validation_rules, False, ':')
    context.collex_id = add_collex(context.survey_id)

    upload_sample_file(context.collex_id, sample_file_path)

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


def upload_sample_file(collex_id, sample_file_path):
    multipart_data = MultipartEncoder(fields={
        'file': ('sample_file', open(sample_file_path, 'rb'), 'text/plain')
    })
    url = f'{Config.SUPPORT_TOOL_API}/upload'

    response = requests.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    response.raise_for_status()

    file_id = response.json()

    form_data = {
        'fileId': file_id,
        'fileName': 'sample_file',
        'collectionExerciseId': collex_id
    }

    create_job_url = f'{Config.SUPPORT_TOOL_API}/job'
    response = requests.post(create_job_url, params=form_data)
    response.raise_for_status()

    job_id = response.json()

    get_job_url = f'{Config.SUPPORT_TOOL_API}/job/{job_id}'

    deadline = time.time() + 30
    sample_validated = False

    while time.time() < deadline:
        response = requests.get(get_job_url)
        response.raise_for_status()

        if response.json().get("jobStatus") == "VALIDATED_OK":
            sample_validated = True
            break
        else:
            time.sleep(1)

    if sample_validated:
        process_job_url = f'{Config.SUPPORT_TOOL_API}/job/{job_id}/process'
        response = requests.post(process_job_url)
        response.raise_for_status()
    else:
        test_helper.fail("Sample did not pass validation before timeout")


@step(
    'sample file "{sample_file_name}" with sensitive columns {sensitive_columns} is loaded successfully')
def load_sample_file_step_for_sensitive_data_multi_column(context, sample_file_name, sensitive_columns):
        sample_file_path = Config.RESOURCE_FILE_PATH.joinpath('sample_files', sample_file_name)
        sample_rows, sample_validation_rules = get_sample_rows_and_validation_rules(sample_file_path, sensitive_columns)

        context.survey_id = add_survey(sample_validation_rules)
        context.collex_id = add_collex(context.survey_id)

        upload_sample_file(context.collex_id, sample_file_path)

        context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows, sensitive_columns)
