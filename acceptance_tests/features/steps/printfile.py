from behave import step


@step("a print file is created")
def creating_print_file(context):
    pack_code = 'pack_code'
    print_file_row = f'{context.sample_units[0]["sample"]["addressLine1"]}|' \
                     f'{context.sample_units[0]["sample"]["postcode"]}|' \
                     f'{context.uac}'

