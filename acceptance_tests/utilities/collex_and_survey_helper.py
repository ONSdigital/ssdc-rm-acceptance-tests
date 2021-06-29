import uuid
from datetime import datetime

import requests
from config import Config


def add_survey(context):
    context.survey_id = str(uuid.uuid4())
    context.survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL}/surveys'

    body = {"id": context.survey_id,
            "name": context.survey_name,
            "sampleValidationRules":
                [
                    {
                        "columnName": "ADDRESS_LINE1",
                        "rules": [
                            {
                                "className": "uk.gov.ons.ssdc.supporttool.validation.MandatoryRule"
                            },
                            {
                                "className": "uk.gov.ons.ssdc.supporttool.validation.LengthRule",
                                "maxLength": 60
                            }
                        ]
                    },
                    {
                        "columnName": "ADDRESS_LINE2",
                        "rules": [
                            {
                                "className": "uk.gov.ons.ssdc.supporttool.validation.LengthRule",
                                "maxLength": 60
                            }
                        ]
                    },
                    {
                        "columnName": "TOWN_NAME",
                        "rules": [
                            {
                                "className": "uk.gov.ons.ssdc.supporttool.validation.MandatoryRule"
                            }
                        ]
                    },
                    {
                        "columnName": "POSTCODE",
                        "rules": [
                            {
                                "className": "uk.gov.ons.ssdc.supporttool.validation.MandatoryRule"
                            },
                            {
                                "className": "uk.gov.ons.ssdc.supporttool.validation.AlphanumericRule"
                            }
                        ]
                    }
                ]}

    response = requests.post(url, auth=Config.BASIC_AUTH, json=body)
    response.raise_for_status()


def add_collex(context):
    context.collex_id = str(uuid.uuid4())
    context.collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL}/collectionExercises'
    body = {'id': context.collex_id, 'name': context.collex_name, 'survey': 'surveys/' + context.survey_id}
    response = requests.post(url, auth=Config.BASIC_AUTH, json=body)
    response.raise_for_status()


def add_survey_and_collex(context):
    add_survey(context)
    add_collex(context)
