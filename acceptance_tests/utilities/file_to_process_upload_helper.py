import os
import time
import uuid
import requests
from requests_toolbelt import MultipartEncoder

from acceptance_tests.utilities import iap_requests
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def upload_file_via_api(collex_id, file_path, job_type, delete_after_upload=False):
    file_name = f'{job_type}_{str(uuid.uuid4())}.csv'

    multipart_data = MultipartEncoder(fields={
        'file': (file_name, open(file_path, 'rb'), 'text/plain')
    })

    url = f'{Config.SUPPORT_TOOL_API}/upload'

    # TODO fix file upload
    # response = requests.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    response = iap_requests.make_request(method='POST',
                                         url=url,
                                         headers={'Content-Type': multipart_data.content_type},
                                         data=multipart_data)
    response.raise_for_status()

    # file_id = response.json()
    file_id = str(response.text.strip('"'))

    request_params = {
        'fileId': file_id,
        'fileName': file_name,
        'collectionExerciseId': collex_id,
        'jobType': job_type
    }

    create_job_url = f'{Config.SUPPORT_TOOL_API}/job'
    response = iap_requests.make_request(method='POST', url=create_job_url, params=request_params)
    response.raise_for_status()

    job_id = str(response.text.strip('"'))

    get_job_url = f'{Config.SUPPORT_TOOL_API}/job/{job_id}'

    deadline = time.time() + 30
    file_validated = False

    while time.time() < deadline:
        response = requests.get(get_job_url)
        response.raise_for_status()

        # TODO debug
        print(response.text[:200])

        if response.json().get("jobStatus") == "VALIDATED_OK":
            file_validated = True
            break
        else:
            time.sleep(1)

    if file_validated:
        process_job_url = f'{Config.SUPPORT_TOOL_API}/job/{job_id}/process'
        response = iap_requests.make_request(method='POST', url=process_job_url)
        response.raise_for_status()

        if delete_after_upload:
            os.unlink(file_path)
    else:
        test_helper.fail(f"File did not pass validation before timeout, job response: {response.json()}")
