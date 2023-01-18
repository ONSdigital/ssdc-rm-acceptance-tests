import requests

from config import Config


def reset_eq_stub():
    response = requests.get(f'{Config.EQ_FLUSH_STUB_URL}/log/reset')
    response.raise_for_status()
