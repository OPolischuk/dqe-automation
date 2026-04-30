import pandas as pd
from pathlib import Path

class ParquetReader:
    def __init__(self, base_path: str):
        # Initialize the base path for parquet files
        self.base_path = Path(base_path)

    def read_parquet(self, folder_name: str, start_date: str = None, end_date: str = None):
        """
        Reads parquet files from a specific folder and filters by date range.
        """
        full_path = self.base_path / folder_name
        
        if not full_path.exists():
            raise FileNotFoundError(f"Path not found: {full_path}")

        # Read parquet data using pandas
        df = pd.read_parquet(full_path)

        # Standardizing column names for DQE validation
        df.columns = [str(col).lower().replace(" ", "_").strip() for col in df.columns]

        # Apply date filtering if columns exist
        if "visit_date" in df.columns and start_date and end_date:
            df["visit_date"] = pd.to_datetime(df["visit_date"]).dt.strftime("%Y-%m-%d")
            mask = (df["visit_date"] >= str(start_date)) & (df["visit_date"] <= str(end_date))
            df = df[mask]

        return df.reset_index(drop=True)