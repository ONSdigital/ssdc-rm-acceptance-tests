import json
from typing import Mapping, Tuple
from jwcrypto import jwe, jws

from acceptance_tests.utilities.test_case_helper import test_helper
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


def decrypt_claims_token_and_check_contents(rh_launch_qid: str, case_id: str, collex_id: str, token: str) \
        -> Tuple[str, str]:
    eq_claims = decrypt_signed_jwe(token)
    test_helper.assertEqual(eq_claims['questionnaire_id'], rh_launch_qid,
                            f'Expected to find the correct QID in the claims payload, actual payload: {eq_claims}')
    test_helper.assertEqual(eq_claims['collection_exercise_sid'], collex_id,
                            'Expected to find the correct collection exercise ID in the claims payload, '
                            f'actual payload: {eq_claims}')
    test_helper.assertEqual(eq_claims['case_id'], case_id,
                            f'Expected to find the correct case ID in the claims payload, actual payload: {eq_claims}')
    # Overwrite these values in the context, they are needed for checking the subsequent events
    return eq_claims['tx_id'], eq_claims['user_id']
