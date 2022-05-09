from behave import step
from acceptance_tests.utilities.rh_service_helper import check_case_from_rh_by_attribute_value_matching_case_id
from acceptance_tests.utilities.test_case_helper import test_helper


@step(
    'the rh-service api is polled for attribute "{attribute}" and value "{value}" the correct case is returned')
def get_rh_case_and_check_correct(context, attribute, value):
    case_id_to_match = get_rm_emitted_case_id_by_attribute_value(context, attribute, value)
    check_case_from_rh_by_attribute_value_matching_case_id(attribute, value, case_id_to_match)


def get_rm_emitted_case_id_by_attribute_value(context, attribute, value):
    case_id_to_match = None

    for emitted_case in context.emitted_cases:
        if emitted_case['sample'][attribute] == value:
            case_id_to_match = emitted_case['caseId']

    test_helper.assertIsNotNone(case_id_to_match,
                                f'Failed to find value {value} for attribute {attribute} in loaded sample with RM')

    return case_id_to_match
