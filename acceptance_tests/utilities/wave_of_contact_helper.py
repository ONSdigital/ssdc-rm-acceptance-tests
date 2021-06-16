import random
import string
import uuid
from datetime import datetime

from acceptance_tests.utilities.database_helper import open_write_cursor


def create_wave_of_contact_in_db(context):
    # whilst WOCs are created to get a UAC for example to receipt, a printfile will still be created after
    # that test has finished, this interferes with other tests as the printfile timestamps is often after the start
    # of the next test.  By using a unique random pack_code we have better filter options
    # We can change/remove this if we get UACS differently or a better solution is found
    context.pack_code = 'pack_code_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    if not hasattr(context, 'template'):
        context.template = '["ADDRESS_LINE1", "POSTCODE", "__uac__"]'

    with open_write_cursor() as cur:
        context.woc_uuid = str(uuid.uuid4())
        trigger_date_time = datetime.utcnow()

        wave_of_contact_query = """insert into casev3.wave_of_contact(id, classifiers,has_triggered, pack_code,
        print_supplier,template,trigger_date_time
        ,type,collection_exercise_id) values (%s,'1=1', 'f', %s, 'SUPPLIER_A',%s,%s,'PRINT',%s)"""
        wave_of_contact_vars = (context.woc_uuid, context.pack_code, context.template,
                                trigger_date_time, context.collex_id)
        cur.execute(wave_of_contact_query, vars=wave_of_contact_vars)
