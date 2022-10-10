from datetime import datetime

import requests

from config import Config


def create_export_file_action_rule(collex_id, classifiers, pack_code, uac_metadata=None):
    url = f'{Config.SUPPORT_TOOL_API}/actionRules'
    body = {
        'type': 'EXPORT_FILE',
        'packCode': pack_code,
        'triggerDateTime': f'{datetime.utcnow().isoformat()}Z',
        'classifiers': classifiers,
        'collectionExerciseId': collex_id
    }

    if uac_metadata:
        body['uacMetadata'] = uac_metadata

    response = requests.post(url, json=body)
    response.raise_for_status()
    return pack_code


def setup_deactivate_uac_action_rule(collex_id):
    url = f'{Config.SUPPORT_TOOL_API}/actionRules'
    body = {
        'type': 'DEACTIVATE_UAC',
        'packCode': None,
        'triggerDateTime': f'{datetime.utcnow().isoformat()}Z',
        'classifiers': '',
        'collectionExerciseId': collex_id
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


def setup_sms_action_rule(collex_id, pack_code):
    url = f'{Config.SUPPORT_TOOL_API}/actionRules'

    body = {
        'type': 'SMS',
        'packCode': pack_code,
        'triggerDateTime': f'{datetime.utcnow().isoformat()}Z',
        'classifiers': '',
        'collectionExerciseId': collex_id,
        'phoneNumberColumn': 'mobileNumber',
        'uacMetadata': {"waveOfContact": "1"}
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


def setup_email_action_rule(collex_id, pack_code):
    url = f'{Config.SUPPORT_TOOL_API}/actionRules'

    body = {
        'type': 'EMAIL',
        'packCode': pack_code,
        'triggerDateTime': f'{datetime.utcnow().isoformat()}Z',
        'classifiers': '',
        'collectionExerciseId': collex_id,
        'emailColumn': 'emailAddress',
        'uacMetadata': {"waveOfContact": "1"}
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
