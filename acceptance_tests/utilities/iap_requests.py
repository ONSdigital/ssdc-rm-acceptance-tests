import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from requests import Response


def make_iap_request(url: str, client_id: str, method: str = 'GET', **kwargs) -> Response:
    """Makes a request to an application protected by Identity-Aware Proxy.
    Args:
      url: The Identity-Aware Proxy-protected URL to fetch.
      client_id: The client ID used by Identity-Aware Proxy.
      method: The request method to use
              ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')
      **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                If no timeout is provided, it is set to 90 by default.
    Returns:
      The requests Response object return by the requests call
    """

    # Set the default timeout, if missing
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 90

    # Obtain an OpenID Connect (OIDC) token from metadata server or using service
    # account.
    open_id_connect_token = id_token.fetch_id_token(Request(), client_id)

    if 'content_type' in kwargs:
        headers = {'Authorization': 'Bearer {}'.format(open_id_connect_token),
                   'Content-Type': kwargs.get('content_type')}
    else:
        headers = {'Authorization': 'Bearer {}'.format(open_id_connect_token)}

    # Fetch the Identity-Aware Proxy-protected URL, including an
    # Authorization header containing "Bearer " followed by a
    # Google-issued OpenID Connect token for the service account.
    response = requests.request(
        method, url,
        headers=headers, **kwargs)
    return response
