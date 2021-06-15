import uuid
from datetime import datetime

from acceptance_tests.utilities.database_helper import open_write_cursor


def add_survey_and_collex_to_db(context):
    with open_write_cursor() as cur:
        context.survey_id = str(uuid.uuid4())
        context.survey_name = 'test survey ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        add_survey_query = """INSERT INTO casev3.survey(id, name) VALUES(%s,%s)"""
        survey_vars = (context.survey_id, context.survey_name)
        cur.execute(add_survey_query, vars=survey_vars)

        context.collex_id = str(uuid.uuid4())
        context.collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        add_collex_query = """INSERT INTO casev3.collection_exercise(id, name, survey_id) VALUES(%s, %s, %s)"""
        collex_vars = (context.collex_id, context.collex_name, context.survey_id)
        cur.execute(add_collex_query, collex_vars)
