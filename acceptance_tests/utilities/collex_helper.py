from datetime import datetime

import requests

from config import Config


def add_collex(survey_id):
    collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL_API}/collectionExercises'
    body = {'name': collex_name, 'surveyId': survey_id}
    response = requests.post(url, json=body)
    response.raise_for_status()

    collex_id = response.json()

    return collex_id
