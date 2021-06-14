from datetime import datetime

from acceptance_tests.utilities.rabbit_helper import purge_queues


def before_scenario(context, _):
    context.test_start_local_datetime = datetime.now()
    context.test_start_utc = datetime.utcnow()
    purge_queues()


def after_all(_context):
    purge_queues()
