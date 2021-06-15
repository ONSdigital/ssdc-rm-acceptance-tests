import uuid
from datetime import datetime

from acceptance_tests.utilities.database_helper import connect_to_db


def add_survey_and_collex_to_db(context):
    pg_connection = connect_to_db()
    cur = pg_connection.cursor()

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

    pg_connection.commit()
    cur.close()
    pg_connection.close()