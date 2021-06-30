from behave import step

from acceptance_tests.utilities.wave_of_contact_helper import create_wave_of_contact


@step('a wave of contact has been created with template "{woc_template}" and classifiers "{classifiers}"')
def create_a_wave_of_contact_with_template_and_classifers(context, woc_template, classifiers):
    context.template = woc_template
    context.classifiers = classifiers
    create_wave_of_contact(context)
