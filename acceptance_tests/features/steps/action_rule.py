from behave import step

from acceptance_tests.utilities.action_rule_helper import create_print_action_rule, \
    setup_deactivate_uac_action_rule


@step('a print action rule has been created with classifiers "{classifiers}"')
def create_print_action_rule_with_template_and_classifiers(context, classifiers):
    create_print_action_rule(context.collex_id, classifiers, context.pack_code)


@step('a deactivate uac action rule has been created')
def create_deactivate_uac_action_rule(context):
    setup_deactivate_uac_action_rule(context.collex_id)
