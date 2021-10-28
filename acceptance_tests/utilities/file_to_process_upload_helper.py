import time

import requests
from requests_toolbelt import MultipartEncoder

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def upload_file_via_api(collex_id, file_path, job_type):
    file_name = job_type + '_FILE'

    multipart_data = MultipartEncoder(fields={
        'file': (file_name, open(file_path, 'rb'), 'text/plain')
    })

    url = f'{Config.SUPPORT_TOOL_API}/upload'

    response = requests.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    response.raise_for_status()

    file_id = response.json()

    request_params = {
        'fileId': file_id,
        'fileName': file_name,
        'collectionExerciseId': collex_id,
        'jobType': job_type
    }

    create_job_url = f'{Config.SUPPORT_TOOL_API}/job'
    response = requests.post(create_job_url, params=request_params)
    response.raise_for_status()

    job_id = response.json()

    get_job_url = f'{Config.SUPPORT_TOOL_API}/job/{job_id}'

    deadline = time.time() + 30
    file_validated = False

    while time.time() < deadline:
        response = requests.get(get_job_url)
        response.raise_for_status()

        if response.json().get("jobStatus") == "VALIDATED_OK":
            file_validated = True
            break
        else:
            time.sleep(1)

    if file_validated:
        process_job_url = f'{Config.SUPPORT_TOOL_API}/job/{job_id}/process'
        response = requests.post(process_job_url)
        response.raise_for_status()
    else:
        test_helper.fail("File did not pass validation before timeout")
