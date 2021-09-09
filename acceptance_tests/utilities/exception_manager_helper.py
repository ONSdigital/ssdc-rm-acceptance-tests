import time
import requests

from acceptance_tests.utilities.audit_trail_helper import get_unique_user_email
from config import Config


def quarantine_bad_messages(bad_message_hashes):
    for message_hash in bad_message_hashes:
        skip_request = {
            "messageHash": message_hash,
            "skippingUser": get_unique_user_email()
        }

        response = requests.post(f"{Config.EXCEPTION_MANAGER_URL}/skipmessage", json=skip_request)
        response.raise_for_status()

    time.sleep(3)
    requests.get(f'{Config.EXCEPTION_MANAGER_URL}/reset')


def get_bad_messages_and_clear():
    response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessages/summary')
    response.raise_for_status()
    bad_messages = response.json()

    hashes = [msg['messageHash'] for msg in bad_messages]
    quarantine_bad_messages(hashes)
