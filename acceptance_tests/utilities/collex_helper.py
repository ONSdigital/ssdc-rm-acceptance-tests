from datetime import datetime, timedelta

import requests

from acceptance_tests.utilities.event_helper import get_emitted_collection_exercise_update
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def add_collex(survey_id):
    collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    start_date = datetime.utcnow()

    url = f'{Config.SUPPORT_TOOL_API}/collectionExercises'
    body = {'name': collex_name,
            'surveyId': survey_id,
            'reference': "MVP012021",
            'startDate': f'{start_date.isoformat()}Z',
            'endDate': f'{(start_date + timedelta(days=2)).isoformat()}Z',
            'metadata': {'test': 'passed'}
            }
    response = requests.post(url, json=body)
    response.raise_for_status()

    collex_id = response.json()

    collection_exercise_update_event = get_emitted_collection_exercise_update()
    test_helper.assertEqual(collection_exercise_update_event['name'], collex_name,
                            'Unexpected collection exercise name')
    test_helper.assertEqual(collection_exercise_update_event['surveyId'], survey_id,
                            'Unexpected survey ID')
    test_helper.assertEqual(collection_exercise_update_event['reference'], "MVP012021",
                            'Unexpected reference')
    test_helper.assertEqual(collection_exercise_update_event['startDate'], f'{start_date.isoformat()}Z',
                            'Invalid or missing start date')
    test_helper.assertEqual(collection_exercise_update_event['endDate'],
                            f'{(start_date + timedelta(days=2)).isoformat()}Z',
                            'Invalid or missing end date')
    test_helper.assertEqual(collection_exercise_update_event['metadata'], {'test': 'passed'},
                            'Unexpected metadata')

    return collex_id
