import requests

from acceptance_tests.utilities.test_case_helper import test_helper
from config import Config
from tenacity import retry, wait_fixed, stop_after_delay


@retry(wait=wait_fixed(1), stop=stop_after_delay(30))
def check_case_from_rh_by_attribute_value_matching_case_id(attribute, value, case_id_in_rm):
    response = requests.get(f'{Config.RH_SERVICE_URL}/cases/attribute/{attribute}/{value}')
    response.raise_for_status()
    rh_cases = response.json()

    test_helper.assertGreater(len(rh_cases), 0, "Found Zero cases with value {value} for attribute {attribute} in RH")

    # With multiple runs of the test/sample file there could be > 1 matches for the attrribute value, but not the caseId
    rh_case_ids = [rh_case["caseId"] for rh_case in rh_cases]

    test_helper.assertIn(case_id_in_rm, rh_case_ids, f"Failed to match RM case id {case_id_in_rm} in"
                                                     f" RH case_ids {rh_case_ids}")

