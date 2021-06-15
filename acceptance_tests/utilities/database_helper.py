import contextlib
import time
import psycopg2

from config import Config


def _poll_database_with_timeout(query, query_vars: tuple, result_success_callback, cur, timeout):
    timeout_deadline = time.time() + timeout
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
    with open_write_cursor() as cur:
        _poll_database_with_timeout(query, query_vars, result_success_callback, cur, timeout)


@contextlib.contextmanager
def open_write_cursor(db_host=Config.DB_HOST_CASE, extra_options=""):
    conn = psycopg2.connect(f"dbname='{Config.DB_NAME}' user='{Config.DB_USERNAME}' host='{db_host}' "
                            f"password='{Config.DB_PASSWORD}' port='{Config.DB_PORT}'"
                            f"{Config.DB_CASE_CERTIFICATES}{extra_options}")
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
