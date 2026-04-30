"""
Description: Data Quality checks for facility_name_min_time_spent_per_visit_date dataset.
Requirement(s): TICKET-1234
Author(s): Oleksandr Polishchuk
"""

import pytest

@pytest.fixture(scope='module')
def source_data(db_connection):
    # Fetching source data from PostgreSQL
    source_query = """
        SELECT facility_name, visit_date, MIN(time_spent) as min_time_spent
        FROM facility_logs
        WHERE visit_date BETWEEN '2026-03-10' AND '2026-03-16'
        GROUP BY facility_name, visit_date
    """
    return db_connection.get_data_sql(source_query)

@pytest.fixture(scope='module')
def target_data(parquet_reader):
    # Reading target data from Parquet files
    target_path = 'results/parquet_data/facility_name_min_time_spent_per_visit_date'
    return parquet_reader.read_parquet(target_path, start_date='2026-03-10', end_date='2026-03-16')

@pytest.mark.parquet_data
@pytest.mark.smoke
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    # Smoke Test: Ensure the dataset is not empty
    data_quality_library.check_dataset_is_not_empty(target_data)

@pytest.mark.parquet_data
def test_check_data_completeness(source_data, target_data, data_quality_library):
    # Completeness Test: Compare Source vs Target
    data_quality_library.check_data_completeness(source_data, target_data)

@pytest.mark.parquet_data
def test_check_uniqueness(target_data, data_quality_library):
    # Quality Test: Check for duplicates
    data_quality_library.check_duplicates(target_data)

@pytest.mark.parquet_data
def test_check_not_null_values(target_data, data_quality_library):
    # Validity Test: Check critical columns for NULLs
    columns_to_check = ['facility_name', 'visit_date', 'min_time_spent']
    data_quality_library.check_not_null_values(target_data, columns_to_check)