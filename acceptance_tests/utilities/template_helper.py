import random
import string
import uuid

import requests

from config import Config


def create_template(create_url, pack_code, template, notify_template_id=None, export_file_destination=None):
    body = {
        'template': template,
        'packCode': pack_code,
        'description': "Test description",
        'metadata': {"foo": "bar"}
    }
    if notify_template_id:
        body['notifyTemplateId'] = notify_template_id
        body['notifyServiceRef'] = "test_service"

    if export_file_destination:
        body['exportFileDestination'] = export_file_destination

    response = requests.post(create_url, json=body)
    response.raise_for_status()


def create_export_file_template(template, export_file_destination=Config.SUPPLIER_DEFAULT_TEST):
    pack_code = generate_pack_code('PRINT_')
    url = f'{Config.SUPPORT_TOOL_API}/exportFileTemplates'
    create_template(url, pack_code, template, export_file_destination=export_file_destination)
    return pack_code


def create_sms_template(template):
    pack_code = generate_pack_code('SMS_')
    notify_template_id = str(uuid.uuid4())
    url = f'{Config.SUPPORT_TOOL_API}/smsTemplates'
    create_template(url, pack_code, template, notify_template_id=notify_template_id)
    return pack_code, notify_template_id


def create_email_template(template):
    pack_code = generate_pack_code('EMAIL_')
    notify_template_id = str(uuid.uuid4())
    url = f'{Config.SUPPORT_TOOL_API}/emailTemplates'
    create_template(url, pack_code, template, notify_template_id=notify_template_id)
    return pack_code, notify_template_id


def generate_pack_code(pack_code_prefix):
    # By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    return pack_code_prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
