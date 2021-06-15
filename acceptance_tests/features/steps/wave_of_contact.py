import uuid
from datetime import datetime

from behave import step

from acceptance_tests.utilities.database_helper import _connect_to_db


@step("a wave of contact has been created")
def create_wave_of_contact(context):
    pg_connection = _connect_to_db()
    cur = pg_connection.cursor()

    context.woc_uuid = str(uuid.uuid4())
    trigger_date_time = datetime.utcnow()

    wave_of_contact_query = """insert into casev3.wave_of_contact(id, classifiers,has_triggered, pack_code,
    print_supplier,template,trigger_date_time
    ,type,collection_exercise_id) values (%s,'1=1', 'f', 'pack_code', 'SUPPLIER_A','["__caseref__","ADDRESS_LINE1",
    "POSTCODE", "__uac__"]',%s,'PRINT',%s)"""
    wave_of_contact_vars = (context.woc_uuid, trigger_date_time, context.collex_id)
    cur.execute(wave_of_contact_query, vars=wave_of_contact_vars)

    pg_connection.commit()
    cur.close()
    pg_connection.close()
