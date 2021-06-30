import csv
from pathlib import Path


def get_sample_rows_and_validation_rules(sample_file_path: Path):
    with open(sample_file_path) as sample_file:
        reader = csv.DictReader(sample_file)
        header = reader.fieldnames
        sample_rows = [row for row in reader]

    validation_rules = [{'columnName': column, 'rules': []} for column in header]
    return sample_rows, validation_rules