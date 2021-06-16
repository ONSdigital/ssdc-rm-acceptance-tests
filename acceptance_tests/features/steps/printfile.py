from behave import step
from retrying import retry

from acceptance_tests.utilities.sftp_helper import SftpUtility
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("a print file is created with correct rows")
def creating_print_file(context):

    print_file_row = ''
    template = context.template.replace('[', '').replace(']', '').replace('"','').split(',')

    for key in template:
        if key == '__uac__':
            print_file_row += f'"{context.uac}"'
        else:
            print_file_row += f'"{context.sample_units[0]["attributes"][key]}"|'

    test_printfile(context, context.pack_code, print_file_row)


@retry(retry_on_exception=lambda e: isinstance(e, FileNotFoundError), wait_fixed=1000, stop_max_attempt_number=120)
def test_printfile(context, pack_code, print_file_row):
    actual_file_rows = testing_sftp_stuff(context, pack_code)

    if not actual_file_rows:
        raise FileNotFoundError

    test_helper.assertEquals(actual_file_rows, [print_file_row], 'Print file contents did not match expected')


@retry(retry_on_exception=lambda e: isinstance(e, FileNotFoundError), wait_fixed=1000, stop_max_attempt_number=120)
def testing_sftp_stuff(context, pack_code):
    with SftpUtility() as sftp_utility:
        supplier = Config.SUPPLIERS_CONFIG['SUPPLIER_A'].get('sftpDirectory')
        files = sftp_utility.get_all_files_after_time(context.test_start_local_datetime, pack_code, supplier, 'csv.gpg')
        file_rows = sftp_utility.get_files_content_as_list(files, pack_code, supplier)
        return file_rows
