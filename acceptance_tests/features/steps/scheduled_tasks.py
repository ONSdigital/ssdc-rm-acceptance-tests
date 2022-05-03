import datetime
import uuid

from behave import step
from tenacity import retry, wait_fixed, stop_after_delay

from acceptance_tests.features.steps.export_file import get_export_file_rows
from acceptance_tests.utilities.case_api_helper import get_logged_events_for_case_by_id, \
    check_if_event_list_is_exact_match
from acceptance_tests.utilities.database_helper import open_cursor
from acceptance_tests.utilities.test_case_helper import test_helper


@step("the expected schedule is created against the new case in the database")
def expected_schduled_created_for_case(context):
    expected_scheduled_task_groups = build_expected_schedule(context.schedule_template)["scheduledTaskGroups"]
    actual_scheduled_task_groups = get_actual_schedule(context.emitted_cases[0])

    test_helper.assertEqual(len(expected_scheduled_task_groups), len(actual_scheduled_task_groups),
                            "Expected Task Groups count differ")

    context.actual_scheduled_tasks = []
    indexer = 0

    for expected_scheduled_task_group in expected_scheduled_task_groups:
        actual_scheduled_task_group = actual_scheduled_task_groups[indexer]

        test_helper.assertEqual(expected_scheduled_task_group["name"], actual_scheduled_task_group["name"])

        test_helper.assertEqual(len(expected_scheduled_task_group["scheduledTasks"]),
                                len(actual_scheduled_task_group["scheduledTasks"]))

        task_index = 0

        for expected_task in expected_scheduled_task_group["scheduledTasks"]:
            actual_task = actual_scheduled_task_group["scheduledTasks"][task_index]
            test_helper.assertTrue(is_valid_uuid(actual_task["id"]))
            context.actual_scheduled_tasks.append(actual_task)

            test_helper.assertEqual(actual_task["name"], expected_task["name"])

            actual_date = datetime.datetime.strptime(actual_task["scheduledDateToRun"][:19], '%Y-%m-%dT%H:%M:%S')
            expected_date = expected_task["rmScheduledDateTime"]

            datetime_difference_minutes = (expected_date - actual_date).total_seconds() / 60
            test_helper.assertLessEqual(datetime_difference_minutes, 1)

            task_index = task_index + 1

        indexer = indexer + 1


def build_expected_schedule(schedule_template):
    task_group_start = datetime.datetime.now()

    expected_schedule = {"scheduledTaskGroups": []}

    for schedule_template_task_group in schedule_template["scheduleTemplateTaskGroups"]:
        expected_scheduled_task_group = {"name": schedule_template_task_group["name"],
                                         "dateOffsetFromTaskGroupStart": schedule_template_task_group[
                                             "dateOffsetFromTaskGroupStart"]}
        task_group_start \
            = add_on_dateoffsets(task_group_start, expected_scheduled_task_group["dateOffsetFromTaskGroupStart"])

        expected_scheduled_task_group["scheduledTasks"] = []

        scheduled_tasks_start = task_group_start

        for scheduled_task in schedule_template_task_group["scheduleTemplateTasks"]:
            expected_scheduled_task = {"name": scheduled_task["name"],
                                       "scheduledTaskType": scheduled_task["scheduledTaskType"],
                                       "packCode": scheduled_task["packCode"],
                                       "dateOffSetFromStart": scheduled_task["dateOffSetFromStart"]}

            scheduled_tasks_start = add_on_dateoffsets(scheduled_tasks_start,
                                                       expected_scheduled_task["dateOffSetFromStart"])

            expected_scheduled_task["rmScheduledDateTime"] = scheduled_tasks_start.utcnow()

            expected_scheduled_task_group["scheduledTasks"].append(expected_scheduled_task)

        expected_schedule["scheduledTaskGroups"].append(expected_scheduled_task_group)

    return expected_schedule


def get_actual_schedule(actual_case):
    with open_cursor() as cur:
        cur.execute("SELECT schedule FROM casev3.cases WHERE id = %s", (actual_case["caseId"],))
        result = cur.fetchone()

        return result[0]


def check_scheduled_tasks_in_db_match_schedule_at_start(actual_scheduled_tasks):
    ids = [task["id"] for task in actual_scheduled_tasks]

    db_tasks = []

    for task_id in ids:
        result = get_scheduled_task_by_id(task_id)
        test_helper.assertIsNotNone(result, "Could not find ScheduledTask on table: " + task_id)
        db_tasks.append(result[0])

    return db_tasks


def get_scheduled_task_by_id(task_id):
    with open_cursor() as cur:
        cur.execute("SELECT * FROM casev3.scheduled_tasks WHERE id = %s", (task_id,))
        result = cur.fetchone()

    return result


def add_on_dateoffsets(start_time, offset):
    multiplier = offset["offset"]

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
    scheduled_task_successfully_removed = False

    for task in context.actual_scheduled_tasks:
        task_scheduled_date = datetime.datetime.strptime(task["scheduledDateToRun"][:19], '%Y-%m-%dT%H:%M:%S')

        if task_scheduled_date < datetime.datetime.now():
            result = get_scheduled_task_by_id(task["id"])
            test_helper.assertIsNone(result, f"Found task that we expected to be deleted. ID {task['id']}")
            scheduled_task_successfully_removed = True
            context.scheduled_task_id = task['id']

        else:
            result = get_scheduled_task_by_id(task["id"])
            test_helper.assertIsNotNone(result, f"Could not find task we expected to still exist.  ID {task['id']}")

    test_helper.assertTrue(scheduled_task_successfully_removed, "Sheduled Tasks not removed/processed within time")


@step("the correct export files are created for the schedule")
def correct_exports_for_files_are_created(context):
    actual_task_groups = get_actual_schedule(context.emitted_cases[0])

    for actual_task_group in actual_task_groups:
        for task in actual_task_group["scheduledTasks"]:
            scheduled_date = datetime.datetime.strptime(task["scheduledDateToRun"][:19], '%Y-%m-%dT%H:%M:%S')

            if scheduled_date < datetime.datetime.now():
                actual_export_file_rows = get_export_file_rows(context.test_start_utc_datetime, task['packCode'])
                test_helper.assertIsNotNone(actual_export_file_rows)
                test_helper.assertEqual(actual_export_file_rows, ['"House 7"|"NW16 FNK"'])


@step("check that the event contains the correct scheduled task id")
def check_event_is_created_correctly(context):
    check_if_event_list_is_exact_match(["NEW_CASE", "EXPORT_FILE"], context.emitted_cases[0]['caseId'])
    events = get_logged_events_for_case_by_id(context.emitted_cases[0]['caseId'])
    scheduled_task_event = [event for event in events if event['scheduledTaskId'] is not None]
    test_helper.assertEqual(scheduled_task_event[0]['scheduledTaskId'], context.scheduled_task_id)
