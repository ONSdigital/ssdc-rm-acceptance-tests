import json
import random
import string
import uuid
from datetime import datetime

import requests

from config import Config


def create_wave_of_contact(collex_id, classifiers, template):
    # whilst WOCs are created to get a UAC for example to receipt, a printfile will still be created after
    # that test has finished, this interferes with other tests as the printfile timestamps is often after the start
    # of the next test.
    # By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    pack_code = 'pack_code_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    url = f'{Config.SUPPORT_TOOL}/waveOfContacts'
    body = {
        'id': str(uuid.uuid4()),
        'type': 'PRINT',
        'packCode': pack_code,
        'triggerDateTime': f'{datetime.utcnow().isoformat()}Z',
        'hasTriggered': False,
        'classifiers': classifiers,
        'template': json.loads(template),
        'printSupplier': 'SUPPLIER_A',
        'collectionExercise':  'collectionExercises/' + collex_id
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
