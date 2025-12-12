import requests
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from config import Config

audience = Config.SUPPORT_FRONTEND_IAP_CLIENT_ID

token = id_token.fetch_id_token(Request(), audience)
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(Config.SUPPORT_FRONTEND_URL, headers=headers)
print(response.text)