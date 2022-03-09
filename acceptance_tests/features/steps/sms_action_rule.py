from behave import step
from acceptance_tests.utilities.notify_helper import check_notify_api_called_with_correct_phone_number_and_template_id
from acceptance_tests.utilities.test_case_helper import test_helper


@step('notify api was called with SMS template with phone number "{expected_phone_number}" and child surname "{'
      'expected_child_surname}"')
def check_notify_called_with_correct_phone_number_and_child_surname(context, expected_phone_number,
                                                                    expected_child_surname):
    received_notify_call = check_notify_api_called_with_correct_phone_number_and_template_id(expected_phone_number,
                                                                                             context.notify_template_id)

    test_helper.assertEqual(received_notify_call['personalisation']['__sensitive__.childLastName'],
                            expected_child_surname,
                            f"Incorrect child surname name sent to notify, json sent {received_notify_call}")
