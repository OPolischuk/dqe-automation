import psycopg2
import pandas as pd

class PostgresConnectorContextManager:
    def __init__(self, db_host: str, db_port: str, db_name: str, db_user: str, db_password: str):
        # Initialize database connection parameters
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.connection = None

    def __enter__(self):
        # Establish the connection to the PostgreSQL database
        self.connection = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Ensure the connection is closed when exiting the context
        if self.connection:
            self.connection.close()

    def get_data_sql(self, sql: str):
        # Execute SQL query and return the result as a pandas DataFrame
        # pd.read_sql maps the database result set directly to a DataFrame
        return pd.read_sql(sql, self.connection)