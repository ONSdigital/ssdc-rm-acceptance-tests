import json
import random
import string
import uuid
from datetime import datetime

import requests

from config import Config


def create_print_action_rule(collex_id, classifiers, template):
    # whilst action rules are created to get a UAC for example to receipt, a printfile will still be created after
    # that test has finished, this interferes with other tests as the printfile timestamps is often after the start
    # of the next test.
    # By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    pack_code = 'pack_code_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    url = f'{Config.SUPPORT_TOOL}/actionRules'
    body = {
        'id': str(uuid.uuid4()),
        'type': 'PRINT',
        'packCode': pack_code,
        'triggerDateTime': f'{datetime.utcnow().isoformat()}Z',
        'hasTriggered': False,
        'classifiers': classifiers,
        'template': json.loads(template),
        'printSupplier': 'SUPPLIER_A',
        'collectionExercise': 'collectionExercises/' + collex_id
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
    return pack_code


def setup_deactivate_uac_action_rule(collex_id):
    url = f'{Config.SUPPORT_TOOL}/actionRules'
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
