import requests

from config import Config


def get_logged_events_for_case_by_id(case_id):
    response = requests.get(f'{Config.CASE_API_CASE_URL}{case_id}?caseEvents=true')
    response.raise_for_status()
    response_json = response.json()
    return response_json['caseEvents']
