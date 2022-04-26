import csv
import json
from pathlib import Path
from typing import List

from behave import step

import random
import string

from acceptance_tests.utilities.collex_helper import add_collex
from acceptance_tests.utilities.event_helper import get_emitted_cases
from acceptance_tests.utilities.file_to_process_upload_helper import upload_file_via_api
from acceptance_tests.utilities.sample_helper import read_sample
from acceptance_tests.utilities.survey_helper import add_survey
from acceptance_tests.utilities.test_case_helper import test_helper
from acceptance_tests.utilities.validation_rule_helper import get_sample_header_and_rows, \
    get_sample_rows_and_generate_open_validation_rules, get_sample_sensitive_columns, get_validation_rules
from config import Config

SAMPLE_FILES_PATH = Config.RESOURCE_FILE_PATH.joinpath('sample_files')
VALIDATION_RULES_PATH = Config.RESOURCE_FILE_PATH.joinpath('validation_rules')
SCHEDULE_TEMPLATE_PATH = Config.RESOURCE_FILE_PATH.joinpath('schedule_templates')


def get_emitted_cases_and_check_against_sample(sample_rows, sensitive_columns=[]):
    emitted_cases = get_emitted_cases(len(sample_rows))
    unmatched_sample_rows = sample_rows.copy()
    for emitted_case in emitted_cases:
        matched_row = None
        for sample_row in unmatched_sample_rows:
            if (get_sample_only_data(sample_row, sensitive_columns) ==
                    emitted_case['sample'] and
                    get_expected_emitted_sensitive_data(sample_row, sensitive_columns) ==
                    emitted_case['sampleSensitive']):
                matched_row = sample_row
                break

        if matched_row:
            unmatched_sample_rows.remove(matched_row)
        else:
            test_helper.fail(f"Could not find matching row in the sample data for case: {emitted_case} "
                             f"all emitted cases: {emitted_cases}")

    return emitted_cases


def get_sample_only_data(sample_row, sensitive_columns):
    return {k: v for k, v in sample_row.items() if k not in sensitive_columns}


def get_expected_emitted_sensitive_data(sample_row, sensitive_columns):
    sensitive_only = {k: v for k, v in sample_row.items() if k in sensitive_columns}

    for key, value in sensitive_only.items():
        if value:
            sensitive_only[key] = 'REDACTED'
        else:
            sensitive_only[key] = ''

    return sensitive_only


@step('BOM sample file "{sample_file_name}" is loaded successfully')
def load_bom_sample_file_step(context, sample_file_name):
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_generate_open_validation_rules(sample_file_path)

    # Fix the BOM mess
    sample_validation_rules[0]['columnName'] = 'TLA'
    for index in range(len(sample_rows)):
        sample_rows[index]['TLA'] = sample_rows[index].pop('\ufeffTLA')

    context.survey_id = add_survey(sample_validation_rules)
    context.expected_collection_instrument_url = "http://test-eq.com/test-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        }
    ]
    context.collex_id = add_collex(context.survey_id, collection_instrument_selection_rules)

    upload_file_via_api(context.collex_id, sample_file_path, 'SAMPLE')

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


@step('sample file "{sample_file_name}" is loaded successfully')
def load_sample_file_step(context, sample_file_name):
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_generate_open_validation_rules(sample_file_path)

    context.survey_id = add_survey(sample_validation_rules)

    context.expected_collection_instrument_url = "http://test-eq.com/test-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        }
    ]
    context.collex_id = add_collex(context.survey_id, collection_instrument_selection_rules)

    upload_file_via_api(context.collex_id, sample_file_path, 'SAMPLE')

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


@step('sample file "{sample_file_name}" is loaded successfully with complex case CI selection rules')
def load_sample_file_with_complex_case_ci_rules_step(context, sample_file_name):
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_generate_open_validation_rules(sample_file_path)

    context.survey_id = add_survey(sample_validation_rules)

    context.expected_collection_instrument_url = "http://test-eq.com/complex-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 100,
            "spelExpression": "caze.sample['POSTCODE'] == 'NW16 FNK'",
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        },
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": "this URL should not be chosen. If it is, the test is a failure"
        }
    ]
    context.collex_id = add_collex(context.survey_id, collection_instrument_selection_rules)

    upload_file_via_api(context.collex_id, sample_file_path, 'SAMPLE')

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


@step('sample file "{sample_file_name}" is loaded successfully with complex UAC CI selection rules')
def load_sample_file_with_complex_uac_ci_rules_step(context, sample_file_name):
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_generate_open_validation_rules(sample_file_path)

    context.survey_id = add_survey(sample_validation_rules)

    context.expected_collection_instrument_url = "http://test-eq.com/super-complex-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 200,
            "spelExpression": "caze.sample['POSTCODE'] == 'NW16 FNK' and uacMetadata['waveOfContact'] == '1'",
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        },
        {
            "priority": 100,
            "spelExpression": "caze.sample['POSTCODE'] == 'NW16 FNK'",
            "collectionInstrumentUrl": "this is a lower priority less specific rule that we don't want"
        },
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": "this URL should not be chosen. If it is, the test is a failure"
        }
    ]
    context.collex_id = add_collex(context.survey_id, collection_instrument_selection_rules)

    upload_file_via_api(context.collex_id, sample_file_path, 'SAMPLE')

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


@step('the sample file "{sample_file_name}"'
      ' with validation rules "{validation_rules_file_name}" is loaded successfully')
def load_sample_file_with_validation_rules_step(context, sample_file_name, validation_rules_file_name):
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    validation_rules_path = VALIDATION_RULES_PATH.joinpath(validation_rules_file_name)
    _, sample_rows = get_sample_header_and_rows(sample_file_path)
    sample_validation_rules = get_validation_rules(validation_rules_path)
    sensitive_columns = get_sample_sensitive_columns(sample_validation_rules)

    context.survey_id = add_survey(sample_validation_rules)
    context.expected_collection_instrument_url = "http://test-eq.com/test-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        }
    ]
    context.collex_id = add_collex(context.survey_id, collection_instrument_selection_rules)

    upload_file_via_api(context.collex_id, sample_file_path, 'SAMPLE')

    context.sample = read_sample(sample_file_path, sample_validation_rules)
    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows, sensitive_columns)


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
    sample_file_path = SAMPLE_FILES_PATH.joinpath('business_rsi_example_sample.csv')
    sample_rows, validation_rules = get_business_sample_columns_and_validation_rules(sample_file_path)

    context.survey_id = add_survey(validation_rules, False, ':')
    context.expected_collection_instrument_url = "http://test-eq.com/test-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        }
    ]
    context.collex_id = add_collex(context.survey_id, collection_instrument_selection_rules)

    upload_file_via_api(context.collex_id, sample_file_path, 'SAMPLE')

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


@step('sample file "{sample_file_name}" with sensitive columns {sensitive_columns:array} is loaded successfully')
def load_sample_file_step_for_sensitive_data_multi_column(context, sample_file_name, sensitive_columns: List):
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_generate_open_validation_rules(sample_file_path,
                                                                                              sensitive_columns)

    context.survey_id = add_survey(sample_validation_rules)
    context.expected_collection_instrument_url = "http://test-eq.com/test-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        }
    ]
    context.collex_id = add_collex(context.survey_id, collection_instrument_selection_rules)

    upload_file_via_api(context.collex_id, sample_file_path, 'SAMPLE')

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows, sensitive_columns)


@step('create survey with template "{schedule_template_file}" and load sample file "{sample_file_name}"')
def load_sample_file_with_schedule_template(context, schedule_template_file, sample_file_name):
    sample_file_path = SAMPLE_FILES_PATH.joinpath(sample_file_name)
    sample_rows, sample_validation_rules = get_sample_rows_and_generate_open_validation_rules(sample_file_path)

    context.schedule_template, context.new_pack_codes = get_schedule_template(schedule_template_file)

    context.survey_id = add_survey(sample_validation_rules, scheduleTemplate=context.schedule_template)

    context.expected_collection_instrument_url = "http://test-eq.com/test-schema"
    collection_instrument_selection_rules = [
        {
            "priority": 0,
            "spelExpression": None,
            "collectionInstrumentUrl": context.expected_collection_instrument_url
        }
    ]
    context.collex_id = add_collex(context.survey_id, collection_instrument_selection_rules)

    upload_file_via_api(context.collex_id, sample_file_path, 'SAMPLE')

    context.emitted_cases = get_emitted_cases_and_check_against_sample(sample_rows)


def get_schedule_template(schedule_template_file):
    schedule_template_path = SCHEDULE_TEMPLATE_PATH.joinpath(schedule_template_file)

    with open(schedule_template_path, 'r') as file:
        schedule_template_str = file.read().replace('\n', '')

    return replace_and_new_packCodes(schedule_template_str)


def replace_and_new_packCodes(schedule_template_str):
    schedule_template = json.loads(schedule_template_str)
    new_pack_codes = []

    for rp_index in range(len(schedule_template["scheduleTemplateTaskGroups"])):
        for st_index in range(len(schedule_template["scheduleTemplateTaskGroups"][rp_index]["scheduleTemplateTasks"])):
            new_pack_code = schedule_template["scheduleTemplateTaskGroups"][rp_index]["scheduleTemplateTasks"][st_index][
                                "packCode"] + '_' + ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=10))
            schedule_template["scheduleTemplateTaskGroups"][rp_index]["scheduleTemplateTasks"][st_index]["packCode"] = new_pack_code
            new_pack_codes.append(new_pack_code)

    return json.dumps(schedule_template), new_pack_codes
