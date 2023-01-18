from typing import List

import requests
from tenacity import retry, stop_after_delay, wait_fixed

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def check_sms_fulfilment_response(sms_fulfilment_response, template):
    expect_uac_hash_and_qid_in_response = any(
        template_item in template for template_item in ['__qid__', '__uac__'])

    if expect_uac_hash_and_qid_in_response:
        test_helper.assertTrue(sms_fulfilment_response['uacHash'],
                               f"sms_fulfilment_response uacHash not found: {sms_fulfilment_response}")
        test_helper.assertTrue(sms_fulfilment_response['qid'],
                               f"sms_fulfilment_response qid not found: {sms_fulfilment_response}")
    else:
        test_helper.assertFalse(
            sms_fulfilment_response)  # Empty JSON is expected response for non-UAC/QID template


def check_email_fulfilment_response(email_fulfilment_response, template):
    expect_uac_hash_and_qid_in_response = any(
        template_item in template for template_item in ['__qid__', '__uac__'])

    if expect_uac_hash_and_qid_in_response:
        test_helper.assertTrue(email_fulfilment_response['uacHash'],
                               f"email_fulfilment_response uacHash not found: {email_fulfilment_response}")
        test_helper.assertTrue(email_fulfilment_response['qid'],
                               f"email_fulfilment_response qid not found: {email_fulfilment_response}")
    else:
        test_helper.assertFalse(
            email_fulfilment_response)  # Empty JSON is expected response for non-UAC/QID template


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def check_notify_api_called_with_correct_phone_number_and_template_id(phone_number, notify_template_id):
    response = requests.get(f'{Config.NOTIFY_STUB_SERVICE}/log/sms')
    test_helper.assertEqual(response.status_code, 200, "Unexpected status code")
    response_json = response.json()
    test_helper.assertEqual(len(response_json), 1, f"Incorrect number of responses, response json {response_json}")
    test_helper.assertEqual(response_json[0]["phone_number"], phone_number, "Incorrect phone number, "
                                                                            f'response json {response_json}')
    test_helper.assertEqual(response_json[0]["template_id"], notify_template_id,
                            f"Incorrect Gov Notify template Id, response json {response_json}")

    return response_json[0]


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def check_notify_api_called_with_correct_email_and_template_id(email, notify_template_id):
    response = requests.get(f'{Config.NOTIFY_STUB_SERVICE}/log/email')
    test_helper.assertEqual(response.status_code, 200, "Unexpected status code")
    response_json = response.json()
    test_helper.assertEqual(len(response_json), 1, f"Incorrect number of responses, response json {response_json}")
    test_helper.assertEqual(response_json[0]["email_address"], email, "Incorrect email, "
                                                                      f'response json {response_json}')
    test_helper.assertEqual(response_json[0]["template_id"], notify_template_id,
                            f"Incorrect Gov Notify template Id, response json {response_json}")

    return response_json[0]


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def retrieve_one_expected_notify_api_email_call():
    response = requests.get(f'{Config.NOTIFY_STUB_SERVICE}/log/email')
    test_helper.assertEqual(response.status_code, 200, "Unexpected status code")
    response_json = response.json()
    test_helper.assertEqual(len(response_json), 1, f"Incorrect number of responses, response json {response_json}")

    return response_json[0]


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def check_notify_api_email_request_calls(email_addresses: List, notify_template_id):
    expected_number_of_calls = len(email_addresses)
    response = requests.get(f'{Config.NOTIFY_STUB_SERVICE}/log/email')
    test_helper.assertEqual(response.status_code, 200, "Unexpected status code")
    response_json = response.json()
    test_helper.assertEqual(len(response_json), expected_number_of_calls,
                            f"Incorrect number of responses, response json {response_json}")

    actual_email_addresses = {call_log_entry['email_address'] for call_log_entry in response_json}
    expected_email_addresses = set(email_addresses)
    test_helper.assertEqual(actual_email_addresses, expected_email_addresses,
                            f'Log of actual email addresses in notify API calls must match expected,'
                            f' response json: {response_json}')
    for call_log_entry in response_json:
        test_helper.assertEqual(call_log_entry["template_id"], notify_template_id,
                                f"Incorrect Gov Notify template Id, response json {call_log_entry}")

    return response_json


def reset_notify_stub():
    requests.get(f'{Config.NOTIFY_STUB_SERVICE}/reset')
