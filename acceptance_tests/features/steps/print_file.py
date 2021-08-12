import json
import random
import string
import uuid
from typing import Iterable

import requests
from behave import step
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed

from acceptance_tests.utilities.sftp_helper import SftpUtility
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_uac_by_case_id(uac_updated_events, case_id):
    for uac_dto in uac_updated_events:
        if uac_dto['caseId'] == case_id:
            return uac_dto['uac']

    test_helper.fail(f"Couldn't find event with case ID: {case_id} in UAC_UPDATED events")


def get_qid_by_case_id(uac_updated_events, case_id):
    for uac_dto in uac_updated_events:
        if uac_dto['caseId'] == case_id:
            return uac_dto['questionnaireId']

    test_helper.fail(f"Couldn't find event with case ID: {case_id} in UAC_UPDATED events ")


@step("a print file is created with correct rows")
def check_print_file_in_sftp(context):
    template = context.template.replace('[', '').replace(']', '').replace('"', '').split(',')
    emitted_uacs = context.emitted_uacs if hasattr(context, 'emitted_uacs') else None
    test_helper.assertFalse(('__uac__' in template or '__qid__' in template) and not emitted_uacs,
                            'Print file template expects UACs or QIDs but no corresponding emitted_uacs found in '
                            'the scenario context')

    expected_print_file_rows = generate_expected_print_file_rows(template,
                                                                 context.emitted_cases,
                                                                 emitted_uacs)

    actual_print_file_rows = get_print_file_rows_from_sftp(context.test_start_local_datetime, context.pack_code)
    check_print_file_matches_expected(actual_print_file_rows, expected_print_file_rows)


def generate_expected_print_file_rows(template, cases, uac_updated_events):
    print_file_rows = []

    for case in cases:
        print_row_components = []
        for field in template:
            if field == '__uac__':
                uac = get_uac_by_case_id(uac_updated_events, case['caseId'])
                print_row_components.append(uac)
            elif field == '__qid__':
                qid = get_qid_by_case_id(uac_updated_events, case['caseId'])
                print_row_components.append(qid)
            else:
                print_row_components.append(case["sample"][field])
        print_file_rows.append(format_expected_print_file_row(print_row_components))
    return print_file_rows


def format_expected_print_file_row(print_row_components: Iterable[str]):
    # The print file format is tab separated and always double quote wrapped CSV
    return '|'.join(f'"{component}"' for component in print_row_components)


def check_print_file_matches_expected(actual_print_file, expected_print_file):
    actual_print_file.sort()
    expected_print_file.sort()

    test_helper.assertEquals(actual_print_file, expected_print_file, 'Print file contents did not match expected')


@retry(retry=retry_if_exception_type(FileNotFoundError), wait=wait_fixed(1), stop=stop_after_delay(120))
def get_print_file_rows_from_sftp(after_datetime, pack_code):
    with SftpUtility() as sftp_utility:
        supplier = Config.SUPPLIERS_CONFIG['SUPPLIER_A'].get('sftpDirectory')
        files = sftp_utility.get_all_files_after_time(after_datetime, pack_code, supplier, 'csv.gpg')
        print_file_rows = sftp_utility.get_files_content_as_list(files, pack_code, supplier)
        if not print_file_rows:
            raise FileNotFoundError
        return print_file_rows


@step('a print template has been created with template "{template}"')
def create_print_template(context, template):
    context.template = template

    # By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    context.pack_code = 'pack_code_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    url = f'{Config.SUPPORT_TOOL_API}/printTemplates'
    body = {
        'packCode': context.pack_code,
        'printSupplier': 'SUPPLIER_A',
        'template': json.loads(template)
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


@step('a sms template has been created with template "{template}"')
def create_print_template(context, template):
    context.template = template

    # By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    context.pack_code = 'pack_code_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    url = f'{Config.SUPPORT_TOOL_API}/smsTemplates'
    body = {
        'templateId': str(uuid.uuid4()),
        'template': json.loads(context.template),
        'packCode': context.pack_code
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
