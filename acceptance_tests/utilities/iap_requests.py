import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from config import Config


def make_request(method: str = "GET", url: str = None, **kwargs) -> requests.Response:
    """Make an IAP authorized request if IAP config is present,
    otherwise fall back on a regular, unauthenticated request
    Kwargs:
      method: The request method to use
              ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')
      url: The Identity-Aware Proxy-protected URL to fetch.
      **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
    """
    #TODO Remove debug
    if Config.IAP_CLIENT_ID:
        response = _make_iap_request(method, url, **kwargs)
    else:
        response = requests.request(method, url, **kwargs)
    print(response.text, response.status_code, response.headers)
    return response

def _make_iap_request(method: str = 'GET', url: str = None, **kwargs) -> requests.Response:
    """Makes a request to an application protected by Identity-Aware Proxy.
    Args:
      method: The request method to use
              ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')
      url: The Identity-Aware Proxy-protected URL to fetch.
      **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                If no timeout is provided, it is set to 90 by default.
    Returns:
      The requests Response object return by the requests call
    """

    # Set the default timeout, if missing
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 90

    # Obtain an OpenID Connect (OIDC) token from metadata server or using service account.
    open_id_connect_token = id_token.fetch_id_token(Request(), Config.IAP_CLIENT_ID)

    # Initialise headers if none are passed in the kwargs
    if 'headers' not in kwargs:
        kwargs['headers'] = {}

    # Set an authorization header containing "Bearer " followed by a
    # Google-issued OpenID Connect token for the service account.
    kwargs['headers']['Authorization'] = f'Bearer {open_id_connect_token}'

    return requests.request(
        method, url, **kwargs)
