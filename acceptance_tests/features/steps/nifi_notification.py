from typing import Mapping

from behave import step

from acceptance_tests.utilities.pubsub_helper import get_matching_pubsub_message_acking_others
from config import Config


@step('a notification PubSub message is sent to NIFI with the correct export file details')
def check_nifi_export_file_notification_message(context):
    def _match_message_file_name_prefix(message: Mapping) -> tuple[bool, str]:
        message_file_name = message['files'][0]['name']
        expected_prefix = f'internal_reprographics/print_services/{context.pack_code}'
        return message_file_name.startswith(expected_prefix), \
            f'Notification message file "{message_file_name}" does not have the expected prefix "{expected_prefix}"'

    get_matching_pubsub_message_acking_others(subscription=Config.PUBSUB_NIFI_INTERNAL_PRINT_NOTIFICATION_SUBSCRIPTION,
                                              message_matcher=_match_message_file_name_prefix,
                                              test_start_time=context.test_start_utc_datetime)
