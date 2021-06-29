import uuid
from datetime import datetime

import requests

from acceptance_tests.utilities.database_helper import open_write_cursor
from config import Config


# def add_survey_and_collex_to_db(context):
#     with open_write_cursor() as cur:
#         context.survey_id = str(uuid.uuid4())
#         context.survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
#         add_survey_query = """INSERT INTO casev3.survey(id, name) VALUES(%s,%s)"""
#         survey_vars = (context.survey_id, context.survey_name)
#         cur.execute(add_survey_query, vars=survey_vars)
#
#         context.collex_id = str(uuid.uuid4())
#         context.collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
#         add_collex_query = """INSERT INTO casev3.collection_exercise(id, name, survey_id) VALUES(%s, %s, %s)"""
#         collex_vars = (context.collex_id, context.collex_name, context.survey_id)
#         cur.execute(add_collex_query, collex_vars)


def add_survey(context):
    context.survey_id = str(uuid.uuid4())
    context.survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL}/surveys'
    body = {'id': context.survey_id, 'name': context.survey_name}
    response = requests.post(url, auth=Config.BASIC_AUTH, json=body)
    response.raise_for_status()


def add_collex(context):
    context.collex_id = str(uuid.uuid4())
    context.collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL}/collectionExercises'
    body = {'id': context.collex_id, 'name': context.collex_name, 'survey_id': context.survey_id}
    response = requests.post(url, auth=Config.BASIC_AUTH, json=body)
    response.raise_for_status()


def add_survey_and_collex(context):
    add_survey(context)
    add_collex(context)
