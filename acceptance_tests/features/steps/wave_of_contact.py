
from behave import step

from acceptance_tests.utilities.wave_of_contact_helper import create_wave_of_contact_in_db


@step("a wave of contact has been created")
def create_wave_of_contact(context):
    create_wave_of_contact_in_db(context)
