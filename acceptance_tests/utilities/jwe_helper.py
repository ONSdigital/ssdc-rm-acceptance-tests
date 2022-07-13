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
    jwe_payload = jwe_token.payload

    # Verify Signature
    jws_token = jws.JWS()
    jws_token.deserialize(jwe_payload.decode())
    jws_token.verify(key=VERIFICATION_KEY)

    # Extract and deserialize the payload
    payload = json.loads(jws_token.payload)
    return payload
