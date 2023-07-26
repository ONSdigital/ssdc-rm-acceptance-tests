import datetime
import json
from typing import Mapping
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


def decrypt_claims_token_and_check_contents(rh_launch_qid: str, case_id: str, collex_id: str, collex_end_date: datetime,
                                            token: str, language_code: str) \
        -> Mapping:
    eq_claims = decrypt_signed_jwe(token)
    test_helper.assertEqual(eq_claims['survey_metadata']['data']['qid'], rh_launch_qid,
                            f'Expected to find the correct QID in the claims payload, actual payload: {eq_claims}')

    test_helper.assertEqual(eq_claims['survey_metadata']["receipting_keys"], ['qid'],
                            f'Expected to find the qid as receipting key in claims payload, '
                            f'actual payload: {eq_claims}')
    test_helper.assertEqual(eq_claims['collection_exercise_sid'], collex_id,
                            'Expected to find the correct collection exercise ID in the claims payload, '
                            f'actual payload: {eq_claims}')
    test_helper.assertEqual(eq_claims['case_id'], case_id,
                            f'Expected to find the correct case ID in the claims payload, actual payload: {eq_claims}')

    test_helper.assertEqual(eq_claims["channel"], "RH", f'Expected channel to be RH, actual payload: {eq_claims}')

    test_helper.assertEqual(eq_claims["language_code"], language_code,
                            f'Expected correct language code: actual payload: {eq_claims}')

    expected_response_expires_at_date = collex_end_date + datetime.timedelta(weeks=4)
    test_helper.assertAlmostEqual(datetime.datetime.fromisoformat(eq_claims["response_expires_at"]),
                                  expected_response_expires_at_date,
                                  delta=datetime.timedelta(minutes=1),
                                  msg=f'Expected response_expires_at date to be 4 exactly weeks in future of '
                                      f'collex_end_date (within 1 minute), actual payload: '
                                      f'{eq_claims}')

    return eq_claims
