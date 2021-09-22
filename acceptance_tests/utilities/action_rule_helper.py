import uuid
from datetime import datetime

import requests

from config import Config


def create_print_action_rule(collex_id, classifiers, pack_code):
    url = f'{Config.SUPPORT_TOOL_API}/actionRules'
    body = {
        'id': str(uuid.uuid4()),
        'type': 'PRINT',
        'packCode': pack_code,
        'triggerDateTime': f'{datetime.utcnow().isoformat()}Z',
        'hasTriggered': False,
        'classifiers': classifiers,
        'collectionExercise': 'collectionExercises/' + collex_id
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
    return pack_code


def setup_deactivate_uac_action_rule(collex_id):
    url = f'{Config.SUPPORT_TOOL_API}/actionRules'
    body = {
        'id': str(uuid.uuid4()),
        'type': 'DEACTIVATE_UAC',
        'packCode': None,
        'triggerDateTime': f'{datetime.utcnow().isoformat()}Z',
        'hasTriggered': False,
        'classifiers': '',
        'template': None,
        'printSupplier': None,
        'collectionExercise': 'collectionExercises/' + collex_id
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
