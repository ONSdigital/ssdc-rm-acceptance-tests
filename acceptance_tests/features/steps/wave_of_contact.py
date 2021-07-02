from behave import step

from acceptance_tests.utilities.wave_of_contact_helper import create_wave_of_contact


@step('a print wave of contact has been created with template "{template}" and classifiers "{classifiers}"')
def create_print_wave_of_contact_with_template_and_classifers(context, template, classifiers):
    context.template = template
    context.classifiers = classifiers
    create_wave_of_contact(context.collex_id, classifiers, template)
