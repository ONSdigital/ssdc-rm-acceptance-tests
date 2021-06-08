import uuid

import requests

from config import Config


def add_new_survey_and_collection_exercise(context):
    add_new_survey(context)
    add_new_collex(context)


def add_new_survey(context):
    context.survey_id = str(uuid.uuid4())
    url = f'{Config.CASE_PROCESSOR}/surveys'
    body = {'id': context.survey_id, 'name': 'testing123'}
    response = requests.post(url, auth=Config.BASIC_AUTH, json=body)
    response.raise_for_status()


def add_new_collex(context):
    context.collex_id = str(uuid.uuid4())
    url = f'{Config.CASE_PROCESSOR}/collexes'
    body = {'id': context.collex_id, 'survey_id': context.survey_id}
    response = requests.post(url, auth=Config.BASIC_AUTH, json=body)
    response.raise_for_status()


