import pytest
import re

# 1. file is not empty
@pytest.mark.validate_csv
def test_file_not_empty(csv_data):
    assert len(csv_data) > 0, "Custom Error: CSV file is empty!"

# 2. check the schema (id, name, age, email, is_active)
@pytest.mark.validate_csv
def test_validate_schema(csv_data, validate_schema):
    expected_schema = ['id', 'name', 'age', 'email', 'is_active']
    actual_schema = list(csv_data[0].keys()) if csv_data else []
    validate_schema(actual_schema, expected_schema)

# 3. checking the age (0-100) + SKIP
@pytest.mark.skip(reason="Skipping this test as per task instructions")
@pytest.mark.validate_csv
def test_age_column_valid(csv_data):
    for row in csv_data:
        age = int(row['age'])
        assert 0 <= age <= 100, f"Custom Error: Age {age} is out of range for ID {row['id']}"

# 4. checking email + CUSTOM MARK
@pytest.mark.validate_csv
def test_email_column_valid(csv_data):
    email_regex = r'^\S+@\S+\.\S+$'
    for row in csv_data:
        assert re.match(email_regex, row['email']), f"Custom Error: Invalid email format: {row['email']}"

# 5. checking the duplicates + XFAIL
@pytest.mark.xfail(reason="Duplicates are expected in this version")
@pytest.mark.validate_csv
def test_duplicates(csv_data):
    ids = [row['id'] for row in csv_data]
    assert len(ids) == len(set(ids)), "Custom Error: Duplicate rows found!"

# 6. parametrized test for ID 1 and 2
@pytest.mark.parametrize("user_id, expected_active", [
    ("1", "FALSE"),
    ("2", "TRUE")
])
def test_active_players_parametrized(csv_data, user_id, expected_active):
    user = next((row for row in csv_data if row['id'] == user_id), None)
    assert user is not None, f"Custom Error: User with ID {user_id} not found"
    assert user['is_active'] == expected_active, f"Custom Error: Expected {expected_active} for ID {user_id}"

# 7. test for ID 2 without parameterization (will receive the 'unmarked' marker via hook)
def test_active_player_id_2_simple(csv_data):
    user = next((row for row in csv_data if row['id'] == "2"), None)
    assert user['is_active'] == "True", "Custom Error: ID 2 should be active"