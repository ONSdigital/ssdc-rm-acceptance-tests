from behave import step

from acceptance_tests.utilities.action_rule_helper import create_action_rule


@step('an action rule has been created with template "{action_rule_template}" and classifiers "{classifiers}"')
def create_an_action_rule_with_template_and_classifers(context, action_rule_template, classifiers):
    context.template = action_rule_template
    context.classifiers = classifiers
    create_action_rule(context)
