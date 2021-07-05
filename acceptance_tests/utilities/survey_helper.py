import uuid
from datetime import datetime

import requests

from config import Config


def add_survey(sample_validation_rules):
    survey_id = str(uuid.uuid4())
    survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL}/surveys'

    body = {"id": survey_id,
            "name": survey_name,
            "sampleValidationRules": sample_validation_rules}

    response = requests.post(url, json=body)
    response.raise_for_status()
    return survey_id
