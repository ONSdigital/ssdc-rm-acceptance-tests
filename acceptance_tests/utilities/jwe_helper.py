import json
from typing import Mapping
from jwcrypto import jwe, jws

from config import Config


def decrypt_signed_jwe(signed_jwe: str) -> Mapping:
    # Decrypt
    jwe_token = jwe.JWE()
    jwe_token.deserialize(signed_jwe, key=Config.EQ_DECRYPTION_KEY)

    # Verify Signature
    jws_token = jws.JWS()
    jws_token.deserialize(jwe_token.payload.decode(), key=Config.EQ_VERIFICATION_KEY)

    # Extract, deserialize, and return the payload
    return json.loads(jws_token.payload)
