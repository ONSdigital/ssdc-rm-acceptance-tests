from http import HTTPStatus

import requests
from requests import HTTPError
from tenacity import retry, retry_if_exception, stop_after_delay, wait_fixed

from config import Config


def is_exception_http_unauthorized(ex: BaseException) -> bool:
    return isinstance(ex, HTTPError) and ex.response.status_code == HTTPStatus.UNAUTHORIZED


# Retry on 401 errors as the UAC may not have been ingested into RH before the first attempt
@retry(retry=retry_if_exception(is_exception_http_unauthorized), wait=wait_fixed(1), stop=stop_after_delay(30),
       reraise=True)
def post_to_launch_endpoint(language_code: str, uac: str) -> requests.Response:
    response = requests.post(f'{Config.RH_UI_URL}{language_code}/start/', data={'uac': uac}, allow_redirects=False)
    response.raise_for_status()
    return response
