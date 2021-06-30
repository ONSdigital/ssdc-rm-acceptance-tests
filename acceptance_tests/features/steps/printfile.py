from behave import step
from retrying import retry

from acceptance_tests.utilities.sftp_helper import SftpUtility
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def get_uac_from_case_id(context, caseId):
    for uac_dto in context.uac_created_events:
        if uac_dto["payload"]["uac"]['caseId'] == caseId:
            return uac_dto["payload"]["uac"]['uac']

    test_helper.fail(f"didn't match caseId: {caseId} in context.uac_created_events")


@step("a print file is created with correct rows")
def checking_files_in_sftp(context):
    template = context.template.replace('[', '').replace(']', '').replace('"', '').split(',')
    print_file_rows = getting_expected_print_files(context, template)

    check_print_files_are_as_expected(context, context.pack_code, print_file_rows)


def getting_expected_print_files(context, template):
    template_len = len(template) - 1
    print_file_rows = []

    for emitted_case in context.emitted_cases:
        print_file_row = ''

        for index, key in enumerate(template):
            if key == '__uac__':
                uac = get_uac_from_case_id(context, emitted_case['caseId'])
                print_file_row += f'"{uac}"|'
            else:
                print_file_row += f'"{emitted_case["sample"][key]}"|'
            if index == template_len:
                altered_print_file_row = print_file_row.rstrip(print_file_row[-1])

        print_file_rows.append(altered_print_file_row)

    return print_file_rows


@retry(retry_on_exception=lambda e: isinstance(e, FileNotFoundError), wait_fixed=1000, stop_max_attempt_number=120)
def check_print_files_are_as_expected(context, pack_code, print_file_row):
    actual_file_rows = get_sftp_files_rows(context, pack_code)

    if not actual_file_rows:
        raise FileNotFoundError

    actual_file_rows.sort()
    print_file_row.sort()

    test_helper.assertEquals(actual_file_rows, print_file_row, 'Print file contents did not match expected')


def get_sftp_files_rows(context, pack_code):
    with SftpUtility() as sftp_utility:
        supplier = Config.SUPPLIERS_CONFIG['SUPPLIER_A'].get('sftpDirectory')
        files = sftp_utility.get_all_files_after_time(context.test_start_local_datetime, pack_code, supplier, 'csv.gpg')
        file_rows = sftp_utility.get_files_content_as_list(files, pack_code, supplier)

        return file_rows


@step("a print file is created expected row count of {expected_row_count}")
def check_created_printfile_has_correct_number_of_rows(context, expected_row_count):
    check_right_number_of_lines_written_to_file(context, expected_row_count)


@retry(retry_on_exception=lambda e: isinstance(e, FileNotFoundError), wait_fixed=1000, stop_max_attempt_number=120)
def check_right_number_of_lines_written_to_file(context, expected_row_count):
    actual_file_rows = get_sftp_files_rows(context, context.pack_code)

    if not actual_file_rows:
        raise FileNotFoundError

    test_helper.assertEquals(len(actual_file_rows), int(expected_row_count))
