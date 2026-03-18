from selenium.common import NoSuchElementException


def refresh_page_until_sample_file_loaded(driver):
    driver.reload()
    sample_file_name_element = driver.find_by_id("sample-file-name-value")
    try:
        return sample_file_name_element
    except NoSuchElementException:
        return False