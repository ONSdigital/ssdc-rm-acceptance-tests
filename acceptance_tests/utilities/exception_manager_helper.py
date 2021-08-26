import time
import requests
from config import Config


def quarantine_bad_messages(bad_message_hashes):
    for message_hash in bad_message_hashes:
        response = requests.get(f"{Config.EXCEPTION_MANAGER_URL}/skipmessage/{message_hash}")
        response.raise_for_status()

    time.sleep(1)
    requests.get(f'{Config.EXCEPTION_MANAGER_URL}/reset')


def get_bad_messages_and_clear():
    response = requests.get(f'{Config.EXCEPTION_MANAGER_URL}/badmessages/summary')
    response.raise_for_status()
    bad_messages = response.json()

    hashes = [msg['messageHash'] for msg in bad_messages]
    quarantine_bad_messages(hashes)
