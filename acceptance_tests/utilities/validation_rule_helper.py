import csv
import json
from pathlib import Path


def get_sample_rows_and_generate_open_validation_rules(sample_file_path: Path, sensitive_columns=[]):
    sample_header, sample_rows = get_sample_header_and_rows(sample_file_path)

    validation_rules = [{'columnName': column, 'rules': [], 'sensitive': column in sensitive_columns}
                        for column in sample_header]

    return sample_rows, validation_rules


def get_validation_rules(validation_rules_path: Path):
    return json.loads(validation_rules_path.read_text())


def get_sample_sensitive_columns(validation_rules):
    return tuple(column['columnName'] for column in validation_rules if column.get('sensitive'))


def get_sample_header_and_rows(sample_file_path: Path):
    with open(sample_file_path) as sample_file:
        reader = csv.DictReader(sample_file)
        sample_header = reader.fieldnames
        sample_rows = [row for row in reader]
    return sample_header, sample_rows
