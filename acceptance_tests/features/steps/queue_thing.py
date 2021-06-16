import functools
import json

from behave import step
from acceptance_tests.utilities.rabbit_helper import start_listening_to_rabbit_queue, store_all_msgs_in_context
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config


@step("a uac_updated msg is emitted with active set to false")
def uac_updated_msg_emitted(context):
    emitted_uac = _get_emitted_uac(context)
    test_helper.assertEqual(emitted_uac['caseId'], context.case_id)
    test_helper.assertFalse(emitted_uac['active'], 'The UAC_UPDATED message should active flag "false"')


@step('a case_updated msg is emitted where "{case_field}" is "{expected_field_value}"')
def case_updated_msg_sent_with_values(context, case_field, expected_field_value, address_level=None, case_type=None,
                                      another_qid_needed=None):
    emitted_case = _get_emitted_case(context)

    test_helper.assertEqual(emitted_case['caseId'], context.case_id)
    test_helper.assertEqual(str(emitted_case[case_field]), expected_field_value)


@step("a uac_updated msg is emitted with active set to true")
def check_uac_updated_msg_emitted_with_qid_active(context):
    context.uac_created_events = get_uac_updated_events(context, len(context.sample_units))
    _test_uacs_updated_correct(context)
    uac = context.uac_created[0]

    test_helper.assertTrue(uac['active'])
    context.questionnaire_id = uac['questionnaireId']
    context.case_id = uac['caseId']
    context.uac = uac['uac']


def _test_uacs_updated_correct(context):
    case_ids = set(sample_unit['id'] for sample_unit in context.sample_units)
    test_helper.assertSetEqual(set(uac['payload']['uac']['caseId'] for uac in context.uac_created_events), case_ids)

    test_helper.assertEqual(len(context.uac_created_events), len(context.sample_units))


def _get_emitted_case(context, type_filter='CASE_UPDATED'):
    context.messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_CASE_QUEUE,
                                    functools.partial(
                                        store_all_msgs_in_context, context=context,
                                        expected_msg_count=1,
                                        type_filter=type_filter))

    test_helper.assertEqual(len(context.messages_received), 1)

    return context.messages_received[0]['payload']['collectionCase']


def _get_emitted_uac(context):
    context.messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE,
                                    functools.partial(
                                        store_all_msgs_in_context, context=context,
                                        expected_msg_count=1,
                                        type_filter='UAC_UPDATED'))

    test_helper.assertEqual(len(context.messages_received), 1)

    return context.messages_received[0]['payload']['uac']


def get_uac_updated_events(context, expected_number):
    context.messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE,
                                    functools.partial(store_all_uac_updated_msgs_by_collex_id,
                                                      context=context,
                                                      expected_msg_count=expected_number,
                                                      collex_id=context.collex_id))
    uac_updated_events = context.messages_received.copy()
    context.messages_received = []
    return uac_updated_events


def store_all_uac_updated_msgs_by_collex_id(ch, method, _properties, body, context, expected_msg_count,
                                            collex_id):
    parsed_body = json.loads(body)

    if (parsed_body['event']['type'] == 'UAC_UPDATED' and
            parsed_body['payload']['uac']['collectionExerciseId'] == collex_id):
        context.messages_received.append(parsed_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        # take it, ignore it?

        ch.basic_nack(delivery_tag=method.delivery_tag)

    if len(context.messages_received) == expected_msg_count:
        ch.stop_consuming()
