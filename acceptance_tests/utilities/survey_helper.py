from datetime import datetime
from functools import partial
from typing import Mapping

import requests

from acceptance_tests.utilities.pubsub_helper import get_matching_pubsub_message_acking_others
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def add_survey(sample_validation_rules, sample_definition_url="http://foo.bar.json", sample_has_header_row=True,
               sample_file_separator=',', schedule_template=None):
    survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL_API}/surveys'

    body = {"name": survey_name,
            "sampleValidationRules": sample_validation_rules,
            "sampleWithHeaderRow": sample_has_header_row,
            "sampleSeparator": sample_file_separator,
            "sampleDefinitionUrl": sample_definition_url,
            "metadata": {'foo': 'bar'},
            "scheduleTemplate": schedule_template}

    response = requests.post(url, json=body)
    response.raise_for_status()

    survey_id = response.json()

    survey_update_event = get_emitted_survey_update(survey_name)
    test_helper.assertEqual(survey_update_event['name'], survey_name,
                            'Unexpected survey name')
    test_helper.assertEqual(survey_update_event['sampleDefinitionUrl'], sample_definition_url,
                            'Unexpected sample definition URL')
    test_helper.assertEqual(survey_update_event['metadata'], {'foo': 'bar'},
                            'Unexpected metadata')

    return survey_id


def get_emitted_survey_update(expected_survey_name):
    # Build the matcher with the current expected survey name
    survey_name_matcher = partial(_survey_name_message_matcher, expected_survey_name=expected_survey_name)

    message_received = get_matching_pubsub_message_acking_others(Config.PUBSUB_OUTBOUND_SURVEY_SUBSCRIPTION,
                                                                 survey_name_matcher)

    return message_received['payload']['surveyUpdate']


def _survey_name_message_matcher(message: Mapping, expected_survey_name=None) -> (bool, str):
    if message['payload']['surveyUpdate']['name'] == expected_survey_name:
        return True, ''
    return False, f'Actual survey name "{message["payload"]["surveyUpdate"]["name"]}" ' \
                  f'does not match expected "{expected_survey_name}"'
