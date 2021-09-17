# I played with a dict previously, but over complicating it.
# Hashes were here, but needed explicitly for tests, so should be in context
sent_messages = []


def reset_global_audit_trail():
    global sent_messages
    sent_messages = []


def record_sent_message_and_hash_in_global_audit_trail(message):
    global sent_messages
    sent_messages.append(message)


def get_global_audit_trail_sent_messages():
    global sent_messages

    sent_messages_as_string = f'{sent_messages}'

    return sent_messages_as_string
