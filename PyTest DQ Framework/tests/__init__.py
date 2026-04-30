[pytest]
# Path to the source code to help Python find 'src' package
pythonpath = ..

# Custom markers registration to avoid PytestUnknownMarkWarning
markers =
    parquet_data: verification of parquet files against database or reports
    postgres: tests related to PostgreSQL database

# Default command line arguments (optional)
# addopts = --html=html_report/report.html --self-contained-html