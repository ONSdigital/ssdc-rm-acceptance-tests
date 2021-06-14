import functools
import json
from datetime import datetime

from behave import *

from acceptance_tests.utilities.rabbit_context import RabbitContext
from acceptance_tests.utilities.rabbit_helper import start_listening_to_rabbit_queue, store_all_msgs_in_context
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


def _get_emitted_uac(context):
    context.messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE,
                                    functools.partial(
                                        store_all_msgs_in_context, context=context,
                                        expected_msg_count=1,
                                        type_filter='UAC_UPDATED'))

    test_helper.assertEqual(len(context.messages_received), 1)

    return context.messages_received[0]['payload']['uac']


@step("a uac_updated msg is emitted with active set to true for the receipted qid")
def check_uac_updated_msg_sets_receipted_qid_to_active(context):
    uac = _get_emitted_uac(context)

    # test_helper.assertEqual(uac['caseId'], context.receipting_case['id'])
    # test_helper.assertEquals(uac['questionnaireId'], context.qid_to_receipt)
    test_helper.assertTrue(uac['active'])
    context.questionnaire_id = uac['questionnaireId']


@when("the case has been receipted")
def receipting_case(context):
    message = json.dumps(
        {
            "event": {
                "type": "RESPONSE_RECEIVED",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2021-06-09T14:10:11.910719Z",
                "transactionId": "730af73e-398d-41d2-893a-cd0722151f9c"
            },
            "payload": {
                "response": {
                    "questionnaireId": context.questionnaire_id,
                    "dateTime": "2019-07-07T22:37:11.988+0000"
                }
            }
        })

    with RabbitContext(exchange='') as rabbit:
        rabbit.publish_message(
            message=message,
            content_type='application/json',
            routing_key=Config.RABBITMQ_RESPONSE_QUEUE)

    print(context.questionnaire_id)


@step("a uac_updated msg is emitted with active set to false")
def uac_updated_msg_emitted(context):
    emitted_uac = _get_emitted_uac(context)
    # test_helper.assertEqual(emitted_uac['caseId'], context.first_case['id'])
    test_helper.assertFalse(emitted_uac['active'], 'The UAC_UPDATED message should active flag "false"')



@step('a case_updated msg is emitted where "{case_field}" is "{expected_field_value}"')
@step(
    'a case_updated msg of type "{case_type}" and address level "{address_level}" is emitted where "{case_field}" is '
    '"{expected_field_value}" and qid is "{another_qid_needed}"')
def case_updated_msg_sent_with_values(context, case_field, expected_field_value, address_level=None, case_type=None,
                                      another_qid_needed=None):

    emitted_case = _get_emitted_case(context)

    # test_helper.assertEqual(emitted_case['id'], context.first_case['id'])
    test_helper.assertEqual(str(emitted_case[case_field]), expected_field_value)


def _get_emitted_case(context, type_filter='CASE_UPDATED'):
    context.messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_CASE_QUEUE,
                                    functools.partial(
                                        store_all_msgs_in_context, context=context,
                                        expected_msg_count=1,
                                        type_filter=type_filter))

    test_helper.assertEqual(len(context.messages_received), 1)

    return context.messages_received[0]['payload']['collectionCase']
