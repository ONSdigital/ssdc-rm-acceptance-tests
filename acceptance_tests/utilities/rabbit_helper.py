import functools
import json
import logging
from typing import List

import requests
from structlog import wrap_logger

from acceptance_tests.utilities.rabbit_context import RabbitContext
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def publish_json_message(message, routing_key, exchange=''):
    with RabbitContext(exchange=exchange) as rabbit:
        rabbit.publish_message(
            message=message,
            content_type='application/json',
            routing_key=routing_key)


def start_listening_to_rabbit_queue(queue, on_message_callback, timeout=60):
    rabbit = RabbitContext(queue_name=queue)
    connection = rabbit.open_connection()

    connection.call_later(
        delay=timeout,
        callback=functools.partial(_timeout_callback, rabbit))

    rabbit.channel.basic_consume(
        queue=queue,
        on_message_callback=on_message_callback)
    rabbit.channel.start_consuming()


def purge_queues():
    all_queues = _get_all_queues()
    with RabbitContext() as rabbit:
        for queue in all_queues:
            rabbit.channel.queue_purge(queue=queue)


def _timeout_callback(rabbit):
    logger.error('Timed out waiting for messages')
    rabbit.close_connection()
    test_helper.fail("Didn't find the expected number of messages")


def _get_all_queues():
    uri = f'http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_HTTP_PORT}/api/queues/%2f/'
    response = requests.get(uri, auth=(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
    response.raise_for_status()
    response_data = json.loads(response.content)

    return [queue['name'] for queue in response_data]


def store_in_message_list(ch, method, _properties, body,
                          message_list: List = None,
                          expected_msg_count: int = None,
                          type_filter: str = None):
    """
    Callback function to parse and store rabbit messages in the passed message_list
    Stops consumption once it has stored expected_msg_count number of messages
    If a type_filter is given, only stores events with matching type
    """
    parsed_body = json.loads(body)

    if type_filter is None or parsed_body['event']['type'] == type_filter:
        message_list.append(parsed_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        # take it, ignore it?
        ch.basic_nack(delivery_tag=method.delivery_tag)

    if len(message_list) == expected_msg_count:
        ch.stop_consuming()
