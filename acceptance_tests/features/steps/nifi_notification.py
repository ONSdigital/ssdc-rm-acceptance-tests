from typing import Mapping

from behave import step

from acceptance_tests.utilities.pubsub_helper import get_matching_pubsub_message_acking_others
from config import Config


@step('a notification PubSub message is sent to NIFI with the correct export file details')
def check_nifi_export_file_notification_message(context):
    def _message_matcher(message: Mapping) -> tuple[bool, str]:
        return message['files'][0]['name'].startswith(f'internal_reprographics/print_services/{context.pack_code}'), \
            'Notification message file name prefix did not match the pack code'

    get_matching_pubsub_message_acking_others(
        subscription=Config.PUBSUB_NIFI_INTERNAL_PRINT_NOTIFICATION_SUBSCRIPTION,
        message_matcher=_message_matcher)
