import logging
import random
import string

from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def get_unique_user_email():
    name_part = ''.join(random.choices(string.ascii_lowercase, k=5))
    domain_part = ''.join(random.choices(string.ascii_lowercase, k=5))
    tld_part = ''.join(random.choices(["com", "org", "gov.uk", "io"]))
    return f'{name_part}@{domain_part}.{tld_part}'


def add_random_suffix_to_email(email_address):
    return f'{email_address}@{get_random_alpha_numerics(4)}'


def get_random_alpha_numerics(length=4):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def log_out_user_context_values(context):
    # TODO Could this be combined this with the CODE Style documentation?
    # Set up a list of context vars Name, Type (string/json/list, description)?
    # This would document and allow consistent outputting of these values in one?

    logger.error('Outputting user context vars')

    context_output = "\n"
    context_output += get_context_value(context, 'test_start_utc_datetime')
    context_output += get_context_value(context, 'survey_id')
    context_output += get_context_value(context, 'collex_id')
    context_output += get_context_list_value(context, 'emitted_cases')
    context_output += get_context_list_value(context, 'emitted_uacs')
    context_output += get_context_value(context, 'pack_code')
    context_output += get_context_value(context, 'template')
    context_output += get_context_value(context, 'telephone_capture_request')
    context_output += get_context_value(context, 'notify_template_id')
    context_output += get_context_value(context, 'sms_fulfilment_response_json')
    context_output += get_context_value(context, 'phone_number')
    context_output += get_context_list_value(context, 'message_hashes')
    context_output += get_context_value(context, 'correlation_id')
    context_output += get_context_value(context, 'originating_user')
    context_output += get_context_list_value(context, 'sent_messages')
    context_output += get_context_value(context, 'case_id')
    context_output += get_context_list_value(context, 'bulk_refusals')
    context_output += get_context_list_value(context, 'bulk_invalids')
    context_output += get_context_list_value(context, 'bulk_sample_update')
    context_output += get_context_list_value(context, 'bulk_sensitive_update')
    context_output += get_context_value(context, 'expected_collection_instrument_url')
    context_output += get_context_value(context, 'fulfilment_personalisation')
    context_output += get_context_list_value(context, 'sample')

    logger.error(context_output)


def get_context_value(context, key):
    if not hasattr(context, key):
        return f"context.{key} not set. \n"

    return f'context.{key}:   {getattr(context, key)} \n'


def get_context_list_value(context, key):

    if not hasattr(context, key):
        return f"context.{key} not set. \n"

    context_list_var = getattr(context, key)

    list_values = f'context.{key}, length {len(context_list_var)} \n'

    for i in range(len(context_list_var)):
        list_values += f'   context.{key}{[i]}:   {context_list_var[i]} \n'

    return list_values
