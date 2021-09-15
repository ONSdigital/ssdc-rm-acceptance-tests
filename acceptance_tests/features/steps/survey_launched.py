import hashlib
import json
import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.audit_trail_helper import add_random_suffix_to_email
from acceptance_tests.utilities.pubsub_helper import publish_to_pubsub
from config import Config


@step('a SURVEY_LAUNCH event is received with email address "{email_address}"')
def send_survey_launched(context, email_address):
    context.correlation_id = str(uuid.uuid4())
    context.originating_user = add_random_suffix_to_email(email_address)

    message = _send_survey_launched_message(context.correlation_id, context.originating_user,
                                            context.emitted_uacs[0]['qid'])
    context.sent_messages.append(message)


@step('a bad survey launched event is put on the topic with email address "{email_address}"')
def bad_survey_launched_message(context, email_address):
    message = _send_survey_launched_message(str(uuid.uuid4()), add_random_suffix_to_email(email_address),
                                            "555555")
    context.sent_messages.append(message)
    context.message_hashes = [hashlib.sha256(message.encode('utf-8')).hexdigest()]


def _send_survey_launched_message(correlation_id, originating_user, qid):
    message = json.dumps(
        {
            "header": {
                "version": Config.EVENT_SCHEMA_VERSION,
                "topic": Config.PUBSUB_SURVEY_LAUNCH_TOPIC,
                "source": "RH",
                "channel": "RH",
                "dateTime": f'{datetime.utcnow().isoformat()}Z',
                "messageId": str(uuid.uuid4()),
                "correlationId": correlation_id,
                "originatingUser": originating_user
            },
            "payload": {
                "surveyLaunch": {
                    "qid": qid
                }
            }
        }
    )

    publish_to_pubsub(message, project=Config.PUBSUB_PROJECT, topic=Config.PUBSUB_SURVEY_LAUNCH_TOPIC)
    return message
