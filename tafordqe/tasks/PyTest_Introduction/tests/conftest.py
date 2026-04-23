import pytest
import csv
import os

@pytest.fixture(scope="session")
def csv_path():
    # path
    return "src/data/data.csv"

@pytest.fixture(scope="session")
def csv_data(csv_path):
    if not os.path.exists(csv_path):
        pytest.fail(f"File not found at {csv_path}")
    with open(csv_path, mode='r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

@pytest.fixture(scope="session")
def validate_schema():
    def _validate(actual, expected):
        assert list(actual) == expected, f"Custom Error: Expected {expected}, but got {actual}"
    return _validate

# Hook for automated marks
def pytest_collection_modifyitems(items):
    for item in items:
        custom_markers = [m for m in item.iter_markers() if m.name != "parametrize"]
        if not custom_markers:
            item.add_marker(pytest.mark.unmarked)