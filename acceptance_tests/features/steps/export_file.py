import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pgpy
from behave import step
from google.cloud import storage
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed

from acceptance_tests.utilities import template_helper
from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("an export file is created with correct rows")
def check_export_file(context):
    template = context.template
    emitted_uacs = context.emitted_uacs if hasattr(context, 'emitted_uacs') else None
    fulfilment_personalisation = context.fulfilment_personalisation if hasattr(context,
                                                                               'fulfilment_personalisation') else None

    test_helper.assertFalse(('__uac__' in template or '__qid__' in template) and not emitted_uacs,
                            'Export file template expects UACs or QIDs but no corresponding emitted_uacs found in '
                            f'the scenario context, emitted_uacs {emitted_uacs}')

    supplier = _get_context_export_supplier_or_default(context)

    actual_export_file_rows = get_export_file_rows(context.test_start_utc_datetime, context.pack_code,
                                                   supplier=supplier)

    uacs_from_actual_export_file = _get_unhashed_uacs_from_actual_export_file(
        actual_export_file_rows, template
    ) if '__uac__' in template else []

    expected_export_file_rows = generate_expected_export_file_rows(template,
                                                                   context.emitted_cases,
                                                                   emitted_uacs, uacs_from_actual_export_file,
                                                                   fulfilment_personalisation)

    check_export_file_matches_expected(actual_export_file_rows, expected_export_file_rows)


@step('an export file template has been created with template "{template_name}"')
def create_export_file_template(context, template_name):
    context.template = context.export_file_templates[template_name]['template']
    context.pack_code = context.export_file_packcodes[template_name]['pack_code']


@step('an export file template has been created for the internal reprographics supplier with template {template:array}')
def create_export_file_template_internal_reprographics(context, template: List):
    context.template = template
    context.pack_code = template_helper.create_export_file_template(
        template,
        export_file_destination=Config.SUPPLIER_INTERNAL_REPROGRAPHICS)
    context.export_supplier = Config.SUPPLIER_INTERNAL_REPROGRAPHICS


def _get_context_export_supplier_or_default(context) -> str:
    return context.export_supplier if hasattr(context, 'export_supplier') else Config.SUPPLIER_DEFAULT_TEST


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


def _get_unhashed_uacs_from_actual_export_file(actual_export_file_rows, template):
    export_file_reader = csv.DictReader(actual_export_file_rows, fieldnames=template, delimiter=',')
    next(export_file_reader, None)  # Exclude header row
    return tuple(export_file_row["__uac__"] for export_file_row in export_file_reader)


def generate_expected_export_file_rows(template: List, cases: List, uac_update_events: List, expected_uacs: List,
                                       fulfilment_personalisation: Dict):
    hashed_uac_to_uac = {
        hashlib.sha256(uac.encode('utf-8')).hexdigest(): uac
        for uac in expected_uacs
    }

    if any(field.startswith('__sensitive__.') for field in template):
        with open_cursor() as cur:
            for case in cases:
                cur.execute("SELECT sample_sensitive FROM casev3.cases WHERE id = %s", (case['caseId'],))
                case['sample_sensitive_values'] = cur.fetchone()[0]

    export_file_rows = [format_expected_export_file_row(template)]  # expected header
    for case in cases:
        export_row_components = []
        for field in template:
            if field == '__uac__':
                hashed_uac = get_uac_hash_by_case_id(uac_update_events, case['caseId'])
                export_row_components.append(hashed_uac_to_uac[hashed_uac])
            elif field == '__qid__':
                qid = get_qid_by_case_id(uac_update_events, case['caseId'])
                export_row_components.append(qid)
            elif field.startswith('__request__.'):
                export_row_components.append(fulfilment_personalisation[field.split('.')[1]])
            elif field.startswith('__sensitive__.'):
                export_row_components.append(case["sample_sensitive_values"][field.split('.')[1]])
            else:
                export_row_components.append(case["sample"][field])
        export_file_rows.append(format_expected_export_file_row(export_row_components))
    return export_file_rows


def format_expected_export_file_row(export_row_components: Iterable[str]):
    # The export file format is comma separated and always double quote wrapped CSV
    return ','.join(f'"{component}"' for component in export_row_components)


def check_export_file_matches_expected(actual_export_file, expected_export_file):
    test_helper.assertEqual(actual_export_file[0], expected_export_file[0],
                            'Export file header row did not match expected')

    actual_export_file.sort()
    expected_export_file.sort()

    test_helper.assertEqual(actual_export_file, expected_export_file, 'Export file contents did not match expected')


def get_datetime_from_export_file_name(export_file_name: str, prefix: str, suffix: str) -> datetime:
    raw_datetime = export_file_name[len(prefix):-len(suffix)]  # Strip off the prefix and suffix
    return datetime.strptime(raw_datetime, '%Y-%m-%dT%H-%M-%S').replace(tzinfo=timezone.utc)


def get_export_file_contents_local(after_datetime: datetime, pack_code: str, export_file_destination: str,
                                   suffix: str) -> Optional[str]:
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

    assert len(export_files_after_datetime) == 1, (f'Found more than one export file'
                                                   f' with expected pack code {pack_code},'
                                                   f' found files: {export_files_after_datetime}'
                                                   f' in destination: {Config.FILE_UPLOAD_DESTINATION}')

    return export_files_after_datetime[0].read_text()


def get_export_file_contents_bucket(after_datetime: datetime, pack_code: str, export_file_destination: str,
                                    suffix: str) -> Optional[str]:
    storage_client = storage.Client()
    storage_bucket = storage_client.get_bucket(Config.FILE_UPLOAD_DESTINATION)

    # Export files are named in the format {export_file_destination}/{pack_code}_{datetime}.{suffix}
    destination_and_pack_code_prefix = f'{export_file_destination}/{pack_code}_'
    export_files_after_datetime = tuple(
        blob for blob in storage_bucket.list_blobs(prefix=destination_and_pack_code_prefix)
        if blob.name.endswith(suffix)
        and get_datetime_from_export_file_name(blob.name, destination_and_pack_code_prefix, suffix) >= after_datetime
    )

    if len(export_files_after_datetime) == 0:
        return

    assert len(export_files_after_datetime) == 1, (f'Found more than one export file'
                                                   f' with expected pack code {pack_code},'
                                                   f' found files: {export_files_after_datetime}'
                                                   f' in destination: {Config.FILE_UPLOAD_DESTINATION}')

    matching_export_file_blob = export_files_after_datetime[0]
    export_file_bytes = matching_export_file_blob.download_as_bytes()
    return export_file_bytes.decode()


def get_export_file_contents(after_datetime: datetime, pack_code: str, export_file_destination: str,
                             suffix='.csv.gpg') -> Optional[str]:
    if Config.FILE_UPLOAD_MODE == 'LOCAL':
        return get_export_file_contents_local(after_datetime, pack_code, export_file_destination, suffix)
    return get_export_file_contents_bucket(after_datetime, pack_code, export_file_destination, suffix)


def decrypt_export_file_contents(export_file_contents: str) -> List[str]:
    decrypted_contents = decrypt_message(export_file_contents)
    return decrypted_contents.rstrip().split('\n')


@retry(retry=retry_if_exception_type(FileNotFoundError), wait=wait_fixed(1), stop=stop_after_delay(120))
def get_export_file_rows(after_datetime: datetime, pack_code: str, supplier=Config.SUPPLIER_DEFAULT_TEST) -> List[str]:
    export_file_destination = Config.EXPORT_FILE_DESTINATIONS_CONFIG[supplier].get('exportDirectory')
    encrypted_export_file_contents = get_export_file_contents(after_datetime, pack_code,
                                                              export_file_destination)
    if not encrypted_export_file_contents:
        raise FileNotFoundError

    decrypted_export_file_rows = decrypt_export_file_contents(encrypted_export_file_contents)

    return decrypted_export_file_rows


def decrypt_message(message: str) -> str:
    our_key, _ = pgpy.PGPKey.from_file(Config.OUR_EXPORT_FILE_DECRYPTION_KEY)
    with our_key.unlock(Config.OUR_EXPORT_FILE_DECRYPTION_KEY_PASSPHRASE):
        encrypted_text_message = pgpy.PGPMessage.from_blob(message)
        message_text = our_key.decrypt(encrypted_text_message)

        return message_text.message
