import pytest
import os
from pathlib import Path
from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
from src.connectors.file_system.parquet_reader import ParquetReader
from src.data_quality.data_quality_validation_library import DataQualityLibrary

def pytest_addoption(parser):
    # Registration of command-line options for DB connection
    parser.addoption("--db_host", action="store", default="localhost")
    parser.addoption("--db_port", action="store", default="5434")
    parser.addoption("--db_name", action="store", default="mydatabase")
    parser.addoption("--db_user", action="store", required=True)
    parser.addoption("--db_password", action="store", required=True)

@pytest.fixture(scope='session')
def db_connection(request):
    db_config = {
        "db_host": request.config.getoption("--db_host"),
        "db_port": request.config.getoption("--db_port"),
        "db_name": request.config.getoption("--db_name"),
        "db_user": request.config.getoption("--db_user"),
        "db_password": request.config.getoption("--db_password")
    }
    
    try:
        with PostgresConnectorContextManager(**db_config) as connector:
            yield connector
    except Exception as e:
        # 
        pytest.fail(f"Failed to initialize PostgresConnector: {e}")

@pytest.fixture(scope='session')
def parquet_reader():
    try:
        # root of the project
        base_path = Path(__file__).resolve().parent.parent
        reader = ParquetReader(base_path=str(base_path))
        return reader
    except Exception as e:
        pytest.fail(f"Failed to initialize ParquetReader: {e}")

@pytest.fixture(scope='session')
def data_quality_library():
    return DataQualityLibrary()