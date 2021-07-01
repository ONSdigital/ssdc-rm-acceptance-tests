from behave import step
from retrying import retry

from acceptance_tests.utilities.sftp_helper import SftpUtility
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_uac_by_case_id(uac_updated_events, case_id):
    for uac_dto in uac_updated_events:
        if uac_dto["payload"]["uac"]['caseId'] == case_id:
            return uac_dto["payload"]["uac"]['uac']

    test_helper.fail(f"Couldn't find event with case ID: {case_id} in UAC_UPDATED events")


def get_qid_by_case_id(uac_updated_events, case_id):
    for uac_dto in uac_updated_events:
        if uac_dto["payload"]["uac"]['caseId'] == case_id:
            return uac_dto["payload"]["uac"]['questionnaireId']

    test_helper.fail(f"Couldn't find event with case ID: {case_id} in UAC_UPDATED events ")


@step("a print file is created with correct rows")
def check_print_file_in_sftp(context):
    template = context.template.replace('[', '').replace(']', '').replace('"', '').split(',')
    expected_print_file_rows = generate_expected_print_file_rows(template, context.emitted_cases, context.uac_created_events)

    actual_print_file_rows = get_print_file_rows_from_sftp(context.test_start_local_datetime, context.pack_code)
    check_print_file_matches_expected(actual_print_file_rows, expected_print_file_rows)


def generate_expected_print_file_rows(template, cases, uac_updated_events):
    print_file_rows = []

    for case in cases:
        print_file_components = []
        for field in template:
            if field == '__uac__':
                uac = get_uac_by_case_id(uac_updated_events, case['caseId'])
                print_file_components.append(uac)
            if field == '__qid__':
                qid = get_qid_by_case_id(uac_updated_events, case['caseId'])
                print_file_components.append(qid)
            else:
                print_file_components.append(case["sample"][field])

        print_file_rows = '|'.join(print_file_components)

    return print_file_rows


def check_print_file_matches_expected(actual_print_file, expected_print_file):
    actual_print_file.sort()
    expected_print_file.sort()

    test_helper.assertEquals(actual_print_file, expected_print_file, 'Print file contents did not match expected')


@retry(retry_on_exception=lambda e: isinstance(e, FileNotFoundError), wait_fixed=1000, stop_max_attempt_number=120)
def get_print_file_rows_from_sftp(after_datetime, pack_code):
    with SftpUtility() as sftp_utility:
        supplier = Config.SUPPLIERS_CONFIG['SUPPLIER_A'].get('sftpDirectory')
        files = sftp_utility.get_all_files_after_time(after_datetime, pack_code, supplier, 'csv.gpg')
        print_file_rows = sftp_utility.get_files_content_as_list(files, pack_code, supplier)
        if not print_file_rows:
            raise FileNotFoundError
        return print_file_rows

# @step("a print file is created expected row count of {expected_row_count}")
# def check_created_printfile_has_correct_number_of_rows(context, expected_row_count):
#     check_right_number_of_lines_written_to_file(context, expected_row_count)
#
#
# @retry(retry_on_exception=lambda e: isinstance(e, FileNotFoundError), wait_fixed=1000, stop_max_attempt_number=120)
# def check_right_number_of_lines_written_to_file(context, expected_row_count):
#     actual_file_rows = get_print_file_rows_from_sftp(context, context.pack_code)
#
#     if not actual_file_rows:
#         raise FileNotFoundError
#
#     test_helper.assertEquals(len(actual_file_rows), int(expected_row_count))
