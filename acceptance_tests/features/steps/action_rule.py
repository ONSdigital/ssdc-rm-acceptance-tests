from behave import step

from acceptance_tests.utilities.action_rule_helper import create_print_action_rule, \
    setup_deactivate_uac_action_rule


@step('a print action rule has been created with template "{template}" and classifiers "{classifiers}"')
def create_print_action_rule_with_template_and_classifiers(context, template, classifiers):
    context.template = template
    context.pack_code = create_print_action_rule(context.collex_id, template, classifiers)


@step('a print action rule has been created with template "{template}"')
def create_print_action_rule_with_template(context, template):
    context.template = template
    context.pack_code = create_print_action_rule(context.collex_id, template)


@step('a deactivate uac action rule has been created')
def create_deactivate_uac_action_rule(context):
    setup_deactivate_uac_action_rule(context.collex_id)
