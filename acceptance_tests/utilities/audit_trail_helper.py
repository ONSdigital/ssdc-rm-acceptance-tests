import random
import string


def get_unique_user_email():
    name_part = ''.join(random.choices(string.ascii_lowercase, k=5))
    domain_part = ''.join(random.choices(string.ascii_lowercase, k=5))
    tld_part = ''.join(random.choices(["com", "org", "gov.uk", "io"]))
    return f'{name_part}@{domain_part}.{tld_part}'
