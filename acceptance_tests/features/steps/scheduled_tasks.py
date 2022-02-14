import json
import datetime
import uuid
from tenacity import retry, wait_fixed, stop_after_delay

from behave import *

from acceptance_tests.features.steps.export_file import get_export_file_rows
from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.test_case_helper import test_helper
import pytz

utc=pytz.UTC


@then("the expected schedule is created against the new case in the database")
def expected_schduled_created_for_case(context):
    expected_response_periods = build_expected_schedule(context.schedule_template)["responsePeriods"]
    json_obj = get_actual_schedule(context.emitted_cases[0])

    actual_response_periods = json.loads(json_obj["value"])
    test_helper.assertEqual(len(expected_response_periods), len(actual_response_periods),
                            "ResponsePeriod counts differ")

    context.actual_scheduled_tasks = []

    indexer = 0
    for expected_response_period in expected_response_periods:
        actual_response_period = actual_response_periods[indexer]

        test_helper.assertEqual(expected_response_period["name"], actual_response_period["name"])

        test_helper.assertEqual(len(expected_response_period["scheduledTasks"]),
                                len(actual_response_period["scheduledTasks"]))

        task_index = 0

        for expected_task in expected_response_period["scheduledTasks"]:
            actual_task = actual_response_period["scheduledTasks"][task_index]
            test_helper.assertTrue(is_valid_uuid(actual_task["id"]))
            context.actual_scheduled_tasks.append(actual_task)

            test_helper.assertEqual(actual_task["name"], expected_task["name"])

            # actual_date = datetime.datetime.strptime(actual_task["rmScheduledDateTime"], '%Y-%m-%dT%H:%M:%S.%f%z')
            # expected_date = expected_task["rmScheduledDateTime"]
            # TypeError: can't subtract offset-naive and offset-aware datetimes :(
            # datetime_difference_minutes = (expected_date - actual_date).total_seconds() / 60
            #
            # test_helper.assertLessEqual(datetime_difference_minutes, 1)

            task_index = task_index + 1

        indexer = indexer + 1


def build_expected_schedule(schedule_template_str):
    schedule_template = json.loads(schedule_template_str)

    response_periods_start = datetime.datetime.now()

    expected_schedule = {}
    expected_schedule["responsePeriods"] = []

    for response_period in schedule_template["responsePeriods"]:
        expected_response_period = {}
        expected_response_period["name"] = response_period["name"]
        expected_response_period["dateOffSet"] = {}
        expected_response_period["dateOffSet"] = response_period["dateOffSet"]
        response_periods_start = add_on_dateoffsets(response_periods_start, expected_response_period["dateOffSet"])

        expected_response_period["scheduledTasks"] = []

        scheduled_tasks_start = response_periods_start

        for scheduled_task in response_period["tasks"]:
            expected_scheduled_task = {}

            expected_scheduled_task["name"] = scheduled_task["name"]
            expected_scheduled_task["scheduledTaskType"] = scheduled_task["scheduledTaskType"]
            expected_scheduled_task["packCode"] = scheduled_task["packCode"]
            expected_scheduled_task["receiptRequired"] = scheduled_task["receiptRequired"]

            expected_scheduled_task["dateOffSet"] = scheduled_task["dateOffSet"]
            scheduled_tasks_start = add_on_dateoffsets(scheduled_tasks_start, expected_scheduled_task["dateOffSet"])

            expected_scheduled_task["scheduledTaskStatus"] = "NOT_STARTED"
            expected_scheduled_task["rmScheduledDateTime"] = scheduled_tasks_start.utcnow()
            #   f'{scheduled_tasks_start.utcnow().isoformat()}Z'

            expected_response_period["scheduledTasks"].append(expected_scheduled_task)

        expected_schedule["responsePeriods"].append(expected_response_period)

    return expected_schedule


def get_actual_schedule(actual_case):
    with open_cursor() as cur:
        cur.execute("SELECT schedule FROM casev3.cases WHERE id = %s", (actual_case["caseId"],))
        result = cur.fetchone()

        return result[0]


def check_scheduled_tasks_in_db_match_schedule_at_start(actual_scheduled_tasks):
    ids = [task["id"] for task in actual_scheduled_tasks]

    # kept getting errors trying to do a where in

    db_tasks = []

    for id in ids:
        result = get_scheduled_task_by_id(id)
        test_helper.assertIsNotNone(result, "Could not find ScheduledTask on table: " + id)
        db_tasks.append(result[0])

    return db_tasks


def get_scheduled_task_by_id(id):
    with open_cursor() as cur:
        cur.execute("SELECT * FROM casev3.scheduled_tasks WHERE id = %s", (id,))
        result = cur.fetchone()

    return result


def add_on_dateoffsets(start_time, offset):
    multiplier = offset["multiplier"]

    if offset["dateUnit"] == "DAYS":
        return start_time + datetime.timedelta(days=multiplier)

    if offset["dateUnit"] == "WEEKS":
        return start_time + datetime.timedelta(weeks=multiplier)

    test_helper.fail("Unexpected dateUnit " + offset["dateUnit"])


def is_valid_uuid(value):
    try:
        uuid.UUID(value)

        return True
    except ValueError:
        return False


@step("that the expected scheduledTasks are created in the database")
def checked_scheuled_tasks_actually_scheduled(context):
    check_scheduled_tasks_in_db_match_schedule_at_start(context.actual_scheduled_tasks)


@step("check that a scheduledTask is processed and removed from the database")
def check_processed_scheduled_task_removed_from_db(context):
    scheduled_task_removed(context)


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def scheduled_task_removed(context):
    for task in context.actual_scheduled_tasks:
        task_scheduled_date = datetime.datetime.strptime(task["rmScheduledDateTime"][:19], '%Y-%m-%dT%H:%M:%S')
        # task_scheduled_date = datetime.datetime.strptime(task["rmScheduledDateTime"], '%Y-%m-%dT%H:%M:%S.%f%z')

        if task_scheduled_date < datetime.datetime.now():
            result = get_scheduled_task_by_id(task["id"])
            # need to pad out error message, more date time crap
            test_helper.assertIsNone(result, "Found task that we expected to be deleted")

        else:
            result = get_scheduled_task_by_id(task["id"])
            # need to pad out error message, more date time crap
            test_helper.assertIsNotNone(result, "Could not find task we expected to still exist")


@step("check that the schedule against the case is as expected")
def check_scheduled_is_updated_with_processed_tasks(context):
    check_tasks_updated(context)


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def check_tasks_updated(context):
    json_obj = get_actual_schedule(context.emitted_cases[0])
    actual_response_periods = json.loads(json_obj["value"])

    for response_period in actual_response_periods:
        for task in response_period["scheduledTasks"]:
            scheduled_date = datetime.datetime.strptime(task["rmScheduledDateTime"][:19], '%Y-%m-%dT%H:%M:%S')

            if scheduled_date < datetime.datetime.now():
                # This would need to be more complex with receipt expected
                test_helper.assertEqual(task["scheduledTaskStatus"], "SENT")
            else:
                test_helper.assertEqual(task["scheduledTaskStatus"], "NOT_STARTED")


@step("the correct export files are created for the schedule")
def correct_exports_for_files_are_created(context):
    json_obj = get_actual_schedule(context.emitted_cases[0])
    actual_response_periods = json.loads(json_obj["value"])

    for response_period in actual_response_periods:
        for task in response_period["scheduledTasks"]:
            scheduled_date = datetime.datetime.strptime(task["rmScheduledDateTime"][:19], '%Y-%m-%dT%H:%M:%S')

            if scheduled_date < datetime.datetime.now():
                # An export file should be created for this.  We're only looking for one row.

                pack_code = task['packCode']

                actual_export_file_rows = get_export_file_rows(context.test_start_utc_datetime, task['packCode'])

                test_helper.assertIsNotNone(actual_export_file_rows)
