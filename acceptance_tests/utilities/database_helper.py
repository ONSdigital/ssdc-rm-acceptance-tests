import time
import uuid

import psycopg2
from datetime import datetime

from config import Config


def _connect_to_db():
    return psycopg2.connect(
        f"dbname='{Config.DB_NAME}' user={Config.DB_USERNAME} host='{Config.DB_HOST_CASE}' "
        f"password={Config.DB_PASSWORD} port='{Config.DB_PORT}'{Config.DB_CASE_CERTIFICATES}")


def add_survey_and_collex_to_db(context):
    pg_connection = _connect_to_db()
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


def _poll_database_with_timeout(query, query_vars: tuple, result_success_callback, pg_connection, timeout):
    timeout_deadline = time.time() + timeout
    cur = pg_connection.cursor()
    while True:
        cur.execute(query, vars=query_vars)
        db_result = cur.fetchall()
        if result_success_callback(db_result, timeout_deadline):
            return
        time.sleep(1)


def poll_database_with_timeout(query, query_vars: tuple, result_success_callback, timeout=60):
    """
    A helper function for checking for data changes in the action database within a timeout period
        :param query: The database query to execute
        :param query_vars: Query parameters to pass to the query executor
        :param result_success_callback: A result checking callback function, should return true for success, false for
            failure and fail the tests to break if the timeout deadline is exceeded (it might seem unintuitive that the
            callback checks the timeout but this lets it log the failure reason with access to the data for better
            failure reporting)
            expected signature: example(db_result, timeout_deadline) -> bool
        :param timeout: Timeout period in seconds (default 60s)
        :return: None
    """
    pg_connection = _connect_to_db()
    _poll_database_with_timeout(query, query_vars, result_success_callback, pg_connection, timeout)
#
#
# def poll_case_database_with_timeout(query, query_vars: tuple, result_success_callback, timeout=60):
#     """
#     A helper function for checking for data changes in the case database within a timeout period
#         :param query: The database query to execute
#         :param query_vars: Query parameters to pass to the query executor
#         :param result_success_callback: A result checking callback function, should return true for success, false for
#             failure and fail the tests to break if the timeout deadline is exceeded (it might seem unintuitive that the
#             callback checks the timeout but this lets it log the failure reason with access to the data for better
#             failure reporting)
#             expected signature: example(db_result, timeout_deadline) -> bool
#         :param timeout: Timeout period in seconds (default 60s)
#         :return: None
#     """
#     case_db_conn = psycopg2.connect(
#         f"dbname='{Config.DB_NAME}' user={Config.DB_USERNAME} host='{Config.DB_HOST_CASE}' "
#         f"password={Config.DB_PASSWORD} port='{Config.DB_PORT}'{Config.DB_CASE_CERTIFICATES}")
#     _poll_database_with_timeout(query, query_vars, result_success_callback, case_db_conn, timeout)
