from behave import step

from acceptance_tests.utilities.action_rule_helper import create_export_file_action_rule, \
    setup_deactivate_uac_action_rule, setup_email_action_rule, setup_sms_action_rule, set_eq_flush_action_rule


@step('an export file action rule has been created with classifiers "{classifiers}"')
def create_export_file_action_rule_with_classifiers(context, classifiers):
    context.correlation_id = create_export_file_action_rule(context.collex_id, classifiers, context.pack_code)


@step('an export file action rule has been created')
def create_export_file_action_rule_no_classifiers(context):
    context.correlation_id = create_export_file_action_rule(context.collex_id, '', context.pack_code)


@step('a deactivate uac action rule has been created')
def create_deactivate_uac_action_rule(context):
    context.correlation_id = setup_deactivate_uac_action_rule(context.collex_id)


@step("a SMS action rule has been created")
def create_sms_action_rule(context):
    context.correlation_id = setup_sms_action_rule(context.collex_id, context.pack_code)


@step("an email action rule has been created")
def create_email_action_rule(context):
    context.correlation_id = setup_email_action_rule(context.collex_id, context.pack_code)


@step("an EQ flush action rule has been created")
def create_eq_flush_action_rule(context):
    set_eq_flush_action_rule(context.collex_id)
