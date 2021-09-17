import json
import logging
import time

from google.api_core.exceptions import DeadlineExceeded
from google.cloud import pubsub_v1
from structlog import wrap_logger

from acceptance_tests.utilities.hack_pubsub_audit import record_sent_message_and_hash_in_global_audit_trail
from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def publish_to_pubsub(message, project, topic, **kwargs):
    publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(project, topic)

    future = publisher.publish(topic_path, data=message.encode('utf-8'), **kwargs)

    future.result(timeout=30)
    logger.info("Sent PubSub message", topic=topic, project=project)

    record_sent_message_and_hash_in_global_audit_trail(message)


def purge_outbound_topics():
    _purge_subscription(Config.PUBSUB_OUTBOUND_UAC_SUBSCRIPTION)
    _purge_subscription(Config.PUBSUB_OUTBOUND_CASE_SUBSCRIPTION)


def _purge_subscription(subscription):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(Config.PUBSUB_PROJECT, subscription)

    # TODO - the seek method should be quick and clean, but it doesn't seem reliable in our GCP CI pipeline
    # timestamp = Timestamp()
    # time_a_bit_in_the_future = datetime.utcnow() + timedelta(minutes=5)
    # timestamp.FromDatetime(time_a_bit_in_the_future)
    # try:
    #     # Try purging via the seek method
    #     # Seeking to now should ack any messages published before this moment
    #     subscriber.seek(subscription_path, time=timestamp)
    # except MethodNotImplemented:
    #     # Seek is not implemented by the pubsub-emulator

    # Call ack all with 5 seconds in-between to catch any stubborn stragglers
    _ack_all_on_subscription(subscriber, subscription_path)


def _ack_all_on_subscription(subscriber, subscription_path):
    max_messages_per_attempt = 100

    try:
        response = subscriber.pull(subscription_path, max_messages=max_messages_per_attempt, timeout=2)
    except DeadlineExceeded:
        return

    ack_ids = [message.ack_id for message in response.received_messages]
    if ack_ids:
        subscriber.acknowledge(subscription_path, ack_ids)

    # It's possible (though unlikely) that they could be > max_messages on the topic so keep deleting till empty
    if len(response.received_messages) == max_messages_per_attempt:
        _ack_all_on_subscription(subscriber, subscription_path)


def _pull_exact_number_of_messages(subscriber, subscription_path, expected_msg_count, timeout):
    # Synchronously pull messages one at at time until we either hit the expected number or the timeout passes.
    received_messages = []
    deadline = time.time() + timeout

    # The PubSub subscriber client does not wait the full duration of its timeout before returning if it finds just
    # at least one message. To work around this, we loop pulling messages repeatedly within our own timeout to allow
    # the full time for all the expected messages to be published and pulled
    while len(received_messages) < expected_msg_count and not time.time() > deadline:
        try:
            response = subscriber.pull(subscription_path, max_messages=expected_msg_count, timeout=1)
        except DeadlineExceeded:
            continue
        if response.received_messages:
            subscriber.acknowledge(subscription_path, [message.ack_id for message in response.received_messages])
            received_messages.extend(response.received_messages)

    test_helper.assertEqual(len(received_messages), expected_msg_count,
                            f'Expected to pull exactly {expected_msg_count} message(s) from '
                            f'subscription {subscription_path} but found {len(received_messages)} '
                            f'within the {timeout} second timeout')
    return received_messages


def get_exact_number_of_pubsub_messages(subscription, expected_msg_count, timeout=30):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(Config.PUBSUB_PROJECT, subscription)
    received_messages = _pull_exact_number_of_messages(subscriber, subscription_path, expected_msg_count, timeout)
    parsed_message_bodies = []

    for received_message in received_messages:
        parsed_body = json.loads(received_message.message.data)
        parsed_message_bodies.append(parsed_body)

    subscriber.close()
    return parsed_message_bodies
