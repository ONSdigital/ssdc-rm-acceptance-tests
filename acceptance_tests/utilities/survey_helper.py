import uuid
from datetime import datetime

import requests

from config import Config


def add_survey(sample_validation_rules, sample_has_header_row=True, sample_file_separator=','):
    survey_id = str(uuid.uuid4())
    survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL_API}/surveys'

    body = {"id": survey_id,
            "name": survey_name,
            "sampleValidationRules": sample_validation_rules,
            "sampleWithHeaderRow": sample_has_header_row,
            "sampleSeparator": sample_file_separator}

    response = requests.post(url, json=body)
    response.raise_for_status()
    return survey_id


def add_sis2_survey():
    survey_id = str(uuid.uuid4())
    survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    # sample_validation_rules =

    url = f'{Config.SUPPORT_TOOL_API}/surveys'

    body = {"id": survey_id,
            "name": survey_name,
            "sampleValidationRules": sample_validation_rules,
            "sampleWithHeaderRow": sample_has_header_row,
            "sampleSeparator": sample_file_separator}

    response = requests.post(url, json=body)
    response.raise_for_status()
    return survey_id
