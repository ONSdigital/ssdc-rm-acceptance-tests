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


def get_random_alpha_numerics(length=4):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def add_random_suffix_to_email(email_address):
    return f'{email_address}@{get_random_alpha_numerics(4)}'


def log_out_user_context_values(context):
    # Perhaps combine this with the documentation?
    logger.error("Outputting user context vars")

    logout_context_value(context, 'test_start_local_datetime')
    logout_context_value(context, 'survey_id')
    logout_context_value(context, 'collex_id')
    logout_context_list_value(context, 'emitted_cases')
    logout_context_list_value(context, 'emitted_uacs')
    logout_context_value(context, 'pack_code')
    logout_context_value(context, 'template')
    logout_context_value(context, 'telephone_capture_request')
    logout_context_value(context, 'notify_template_id')
    logout_context_value(context, 'sms_fulfilment_response_json')
    logout_context_value(context, 'phone_number')
    logout_context_list_value(context, 'message_hashes')
    logout_context_value(context, 'correlation_id')
    logout_context_value(context, 'originating_user')
    logout_context_list_value(context, 'sent_messages')


def logout_context_value(context, key):
    if not hasattr(context, key):
        logger.error(f"context.{key} not set.")
        return

    logger.error(f'context.{key}')
    logger.error(f'    {getattr(context, key)}')


def logout_context_list_value(context, key):

    if not hasattr(context, key):
        logger.error(f"context.{key} not set.")
        return

    context_list_var = getattr(context, key)

    logger.error(f'context.{key}, length {len(context_list_var)}')

    for i in range(len(context_list_var)):
        logger.error(f'context.{key}{[i]}:')
        logger.error(f'    {context_list_var[i]}')
