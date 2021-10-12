from datetime import datetime

import requests

from acceptance_tests.utilities.event_helper import get_emitted_survey_update
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def add_survey(sample_validation_rules, sample_has_header_row=True, sample_file_separator=','):
    survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL_API}/surveys'

    body = {"name": survey_name,
            "sampleValidationRules": sample_validation_rules,
            "sampleWithHeaderRow": sample_has_header_row,
            "sampleSeparator": sample_file_separator,
            "sampleDefinitionUrl": "http://foo.bar",
            "metadata": {'foo': 'bar'}}

    response = requests.post(url, json=body)
    response.raise_for_status()

    survey_id = response.json()

    survey_update_event = get_emitted_survey_update()
    test_helper.assertEqual(survey_update_event['name'], survey_name,
                            'Unexpected survey name')
    test_helper.assertEqual(survey_update_event['sampleDefinitionUrl'], "http://foo.bar",
                            'Unexpected sample definition URL')
    test_helper.assertEqual(survey_update_event['metadata'], {'foo': 'bar'},
                            'Unexpected metadata')

    return survey_id
