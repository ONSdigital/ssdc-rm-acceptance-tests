import hashlib
import json
import random
import string
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pgpy
import requests
from behave import step
from google.cloud import storage
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def _get_uac_matching_case_id(uac_update_events, case_id):
    for uac_dto in uac_update_events:
        if uac_dto['caseId'] == case_id:
            return uac_dto

    test_helper.fail(f"Couldn't find event with case ID: {case_id} in UAC_UPDATE events. "
                     f"Full uac_update_events list: {uac_update_events}")


def get_uac_hash_by_case_id(uac_update_events, case_id):
    matching_uac_dto = _get_uac_matching_case_id(uac_update_events, case_id)

    if matching_uac_dto:
        return matching_uac_dto['uacHash']


def get_qid_by_case_id(uac_update_events, case_id):
    matching_uac_dto = _get_uac_matching_case_id(uac_update_events, case_id)

    if matching_uac_dto:
        return matching_uac_dto['qid']


@step("an export file is created with correct rows")
def check_export_file(context):
    template = context.template.replace('[', '').replace(']', '').replace('"', '').split(',')
    emitted_uacs = context.emitted_uacs if hasattr(context, 'emitted_uacs') else None

    test_helper.assertFalse(('__uac__' in template or '__qid__' in template) and not emitted_uacs,
                            'Export file template expects UACs or QIDs but no corresponding emitted_uacs found in '
                            f'the scenario context, emitted_uacs {emitted_uacs}')

    actual_export_file_rows = get_export_file_rows(context.test_start_local_datetime, context.pack_code)

    unhashed_uacs_from_actual_export_file = _get_unhashed_uacs_from_actual_export_file(actual_export_file_rows,
                                                                                       template)

    expected_export_file_rows = generate_expected_export_file_rows(template,
                                                                   context.emitted_cases,
                                                                   emitted_uacs, unhashed_uacs_from_actual_export_file)

    check_export_file_matches_expected(actual_export_file_rows, expected_export_file_rows)


def _get_unhashed_uacs_from_actual_export_file(actual_export_file_rows, template):
    unhashed_uacs_list = []
    for export_file_row in actual_export_file_rows:
        unpacked_export_file = export_file_row.split("|")

        for row, template_column in zip(unpacked_export_file, template):
            if template_column == "__uac__":
                unhashed_uacs_list.append(row)
    return unhashed_uacs_list


def generate_expected_export_file_rows(template, cases, uac_update_events, unhashed_uacs_list):
    export_file_rows = []

    for case in cases:
        export_row_components = []
        for field in template:
            if field == '__uac__':
                hashed_uac = get_uac_hash_by_case_id(uac_update_events, case['caseId'])
                _hashing_expected_uacs(hashed_uac, export_row_components, unhashed_uacs_list)
            elif field == '__qid__':
                qid = get_qid_by_case_id(uac_update_events, case['caseId'])
                export_row_components.append(qid)
            else:
                export_row_components.append(case["sample"][field])
        export_file_rows.append(format_expected_export_file_row(export_row_components))
    return export_file_rows


def _hashing_expected_uacs(hashed_uac, export_row_components, unhashed_uacs_list):
    for unhashed_uac in unhashed_uacs_list:
        temp_hashed_uac = hashlib.sha256(unhashed_uac.strip('"').encode('utf-8')).hexdigest()
        if temp_hashed_uac == hashed_uac:
            export_row_components.append(unhashed_uac.strip('"'))
            break


def format_expected_export_file_row(export_row_components: Iterable[str]):
    # The export file format is tab separated and always double quote wrapped CSV
    return '|'.join(f'"{component}"' for component in export_row_components)


def check_export_file_matches_expected(actual_export_file, expected_export_file):
    actual_export_file.sort()
    expected_export_file.sort()

    test_helper.assertEquals(actual_export_file, expected_export_file, 'Export file contents did not match expected')


def get_datetime_from_export_file_name(export_file_name: str, prefix: str, suffix: str):
    # Export files are named in the format {pack_code}_{datetime}.{suffix}
    raw_datetime = export_file_name.lstrip(prefix).rstrip(suffix)
    return datetime.strptime(raw_datetime, '%Y-%m-%dT%H-%M-%S').astimezone(timezone.utc)


def get_export_file_after_time_local(after_datetime: datetime, pack_code, export_file_destination, suffix):
    destination_path = Path(Config.FILE_UPLOAD_DESTINATION).joinpath(export_file_destination)
    prefix = f'{pack_code}_'
    export_files = destination_path.glob(f'{prefix}*{suffix}')

    # Export files are named in the format {pack_code}_{datetime}.{suffix}
    export_files_after_datetime = tuple(
        export_file for export_file in export_files
        if get_datetime_from_export_file_name(export_file.name, prefix, suffix) >= after_datetime
    )

    if len(export_files_after_datetime) == 0:
        return

    assert len(export_files_after_datetime) <= 1, f'Found more than one export file' \
                                                  f' with expected pack code {pack_code},' \
                                                  f' found files: {export_files_after_datetime}'

    return export_files_after_datetime[0].read_text()


def get_export_file_after_time_bucket(after_datetime: datetime, pack_code, export_file_destination, suffix):
    storage_client = storage.Client()
    storage_bucket = storage_client.get_bucket(Config.FILE_UPLOAD_DESTINATION)

    # Export files are named in the format {export_file_destination}/{pack_code}_{datetime}.{suffix}
    destination_and_pack_code_prefix = f'{export_file_destination}/{pack_code}_'
    export_files_after_datetime = tuple(
        blob for blob in storage_bucket.list_blobs(prefix=destination_and_pack_code_prefix)
        if blob.name.endswith(suffix)
        and datetime.fromisoformat(blob.name.lstrip(destination_and_pack_code_prefix).rstrip(suffix)) >= after_datetime
    )

    if len(export_files_after_datetime) == 0:
        return

    assert len(export_files_after_datetime) <= 1, f'Found more than one export file' \
                                                  f' with expected pack code {pack_code},' \
                                                  f' found files: {export_files_after_datetime}'

    matching_export_file_blob = export_files_after_datetime[0]
    export_file_bytes = matching_export_file_blob.download_as_bytes()
    return export_file_bytes.decode()


def get_encrypted_export_file_after_time(after_datetime: datetime, pack_code, export_file_destination, suffix=''):
    if Config.FILE_UPLOAD_MODE == 'LOCAL':
        return get_export_file_after_time_local(after_datetime, pack_code, export_file_destination, suffix)
    return get_export_file_after_time_bucket(after_datetime, pack_code, export_file_destination, suffix)


def decrypt_export_file_rows(export_file_contents):
    decrypted_contents = decrypt_message(export_file_contents)
    return decrypted_contents.rstrip().split('\n')


@retry(retry=retry_if_exception_type(FileNotFoundError), wait=wait_fixed(1), stop=stop_after_delay(120))
def get_export_file_rows(after_datetime, pack_code, supplier='SUPPLIER_A'):
    export_file_destination = Config.EXPORT_FILE_DESTINATIONS_CONFIG[supplier].get('exportDirectory')
    encrypted_export_file_contents = get_encrypted_export_file_after_time(after_datetime, pack_code,
                                                                          export_file_destination, '.csv.gpg')
    if not encrypted_export_file_contents:
        raise FileNotFoundError

    decrypted_export_file_rows = decrypt_export_file_rows(encrypted_export_file_contents)

    return decrypted_export_file_rows


@step('an export file template has been created with template "{template}"')
def create_export_file_template(context, template):
    context.template = template

    # By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    context.pack_code = 'pack_code_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    url = f'{Config.SUPPORT_TOOL_API}/exportFileTemplates'
    body = {
        'packCode': context.pack_code,
        'exportFileDestination': 'SUPPLIER_A',
        'template': json.loads(template),
        'description': "Test description",
        'metadata': {"foo": "bar"}
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


def decrypt_message(message):
    our_key, _ = pgpy.PGPKey.from_file(Config.OUR_EXPORT_FILE_DECRYPTION_KEY)
    with our_key.unlock(Config.OUR_EXPORT_FILE_DECRYPTION_KEY_PASSPHRASE):
        encrypted_text_message = pgpy.PGPMessage.from_blob(message)
        message_text = our_key.decrypt(encrypted_text_message)

        return message_text.message
