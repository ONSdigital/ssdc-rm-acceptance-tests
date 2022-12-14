from datetime import datetime, timedelta

import requests

from acceptance_tests.utilities.event_helper import get_emitted_collection_exercise_update
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def add_collex(survey_id, collection_instrument_selection_rules):
    collex_name = 'test collex ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=2)

    url = f'{Config.SUPPORT_TOOL_API}/collectionExercises'
    body = {'name': collex_name,
            'surveyId': survey_id,
            'reference': "MVP012021",
            'startDate': f'{start_date.isoformat()}Z',
            'endDate': f'{end_date.isoformat()}Z',
            'collectionInstrumentSelectionRules': collection_instrument_selection_rules
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

    parsed_start_date = datetime.strptime(collection_exercise_update_event['startDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
    parsed_end_date = datetime.strptime(collection_exercise_update_event['endDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    test_helper.assertEqual(parsed_start_date, start_date, 'Invalid or missing start date')
    test_helper.assertEqual(parsed_end_date, end_date, 'Invalid or missing end date')

    # test_helper.assertEqual(collection_exercise_update_event['metadata'], {'test': 'passed'},
    #                         'Unexpected metadata')

    return collex_id
