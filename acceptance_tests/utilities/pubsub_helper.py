import json
import logging

from google.cloud import pubsub_v1
from google.cloud.exceptions import MethodNotImplemented
from google.protobuf.timestamp_pb2 import Timestamp
from structlog import wrap_logger

from config import Config

logger = wrap_logger(logging.getLogger(__name__))

subscriber = pubsub_v1.SubscriberClient()


def publish_to_pubsub(message, project, topic, **kwargs):
    publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(project, topic)

    future = publisher.publish(topic_path, data=message.encode('utf-8'), **kwargs)

    future.result(timeout=30)
    logger.info("Sent PubSub message", topic=topic, project=project)

