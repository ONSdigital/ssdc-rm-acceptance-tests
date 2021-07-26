import uuid
from datetime import datetime

import requests

from config import Config


def add_collex(survey_id):
    collex_id = str(uuid.uuid4())
    collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    url = f'{Config.SUPPORT_TOOL_API}/collectionExercises'
    body = {'id': collex_id, 'name': collex_name, 'survey': 'surveys/' + survey_id}
    response = requests.post(url, json=body)
    response.raise_for_status()
    return collex_id
