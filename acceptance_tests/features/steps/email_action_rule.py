from behave import step

from acceptance_tests.utilities.notify_helper import check_notify_api_called_with_correct_email_and_template_id, \
    check_notify_api_email_request_calls
from acceptance_tests.utilities.test_case_helper import test_helper


@step('notify api was called with email template with email address "{expected_email}" and child surname "{'
      'expected_child_surname}"')
def check_notify_called_with_correct_email_and_child_surname(context, expected_email, expected_child_surname):
    received_notify_call = check_notify_api_called_with_correct_email_and_template_id(expected_email,
                                                                                      context.notify_template_id)

    test_helper.assertEqual(received_notify_call['personalisation']['__sensitive__.childLastName'],
                            expected_child_surname,
                            f"Incorrect child surname name sent to notify, json sent {received_notify_call}")


@step('notify api was called with the correct emails from sample field "{email_column}" and notify template')
def check_notify_called_with_correct_emails_and_uacs(context, email_column: str):
    # Email addresses should always be sensitive
    email_addresses = [sample_row['sensitive'][email_column] for sample_row in context.sample]

    check_notify_api_email_request_calls(email_addresses, context.notify_template_id)
