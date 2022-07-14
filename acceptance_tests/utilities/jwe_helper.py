import json
from typing import Mapping

from jwcrypto import jwe, jwk, jws

from config import Config

DECRYPTION_KEY = jwk.JWK.from_pem(Config.EQ_TOKEN_DECRYPTION_KEY.read_text().encode())
VERIFICATION_KEY = jwk.JWK.from_pem(Config.EQ_TOKEN_VERIFICATION_KEY.read_text().encode())


def decrypt_signed_jwe(signed_jwe: str) -> Mapping:
    # Decrypt
    jwe_token = jwe.JWE()
    jwe_token.deserialize(signed_jwe, key=DECRYPTION_KEY)

    # Verify Signature
    jws_token = jws.JWS()
    jws_token.deserialize(jwe_token.payload.decode(), key=VERIFICATION_KEY)

    # Extract, deserialize, and return the payload
    return json.loads(jws_token.payload)
