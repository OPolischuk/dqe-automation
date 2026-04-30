import pandas as pd
import json
from pathlib import Path

def read_plotly_json(json_string):
    """
    Extracts data from Plotly's JSON structure retrieved via Selenium.
    Converts the internal trace format into a standard Pandas DataFrame.
    """
    if not json_string or json_string == "null":
        raise Exception("Plotly data object not found on the page.")
        
    data = json.loads(json_string)
    
    # Plotly table data is stored in columns within 'header' and 'cells'
    headers = data['header']['values']
    cells = data['cells']['values']
    
    # Transposing column-based data into rows for DataFrame construction
    rows = list(zip(*cells))
    
    df = pd.DataFrame(rows, columns=headers)
    
    # Standardizing column names to snake_case for consistent comparison
    df.columns = [str(col).lower().replace(" ", "_").strip() for col in df.columns]
    
    # Data cleaning: removing HTML tags (e.g., <b>) and whitespace from values
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'<[^>]*>', '', regex=True).str.strip()
        
    return df

def read_parquet_data(folder_path, start_date=None, end_date=None):
    """
    Reads Parquet files from the specified directory and filters by date range.
    Ensures the source data matches the reporting period of the BI report.
    """
    p = Path(folder_path)
    if not p.exists():
        raise FileNotFoundError(f"Path not found: {folder_path}")

    # Reading the entire partition folder into a single DataFrame
    df = pd.read_parquet(folder_path)
    
    # Normalizing column names to match the cleaned HTML report columns
    df.columns = [str(col).lower().replace(" ", "_").strip() for col in df.columns]
    
    # Mapping source field names to reporting field names (DQE requirement)
    mapping = {'avg_time_spent': 'average_time_spent'}
    df = df.rename(columns=mapping)

    # Filtering data by date range to exclude historical or irrelevant partitions
    if "visit_date" in df.columns:
        df["visit_date"] = pd.to_datetime(df["visit_date"]).dt.strftime("%Y-%m-%d")
        
        if start_date and end_date:
            mask = (df["visit_date"] >= str(start_date)) & (df["visit_date"] <= str(end_date))
            df = df[mask]
            
    return df.astype(str).reset_index(drop=True)

def compare_dataframes(df1, df2):
    """
    Performs a strict comparison between the HTML report and the Parquet dataset.
    Aligns columns, sorts rows, and provides a detailed mismatch log if validation fails.
    """
    # Aligning Parquet columns with the HTML report schema
    try:
        df2 = df2[df1.columns].copy()
    except KeyError as e:
        return False, f"Schema mismatch! Parquet missing: {e}"

    # Sorting both datasets to ensure identical row order for comparison
    df1 = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2 = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)

    # Row count validation
    if len(df1) != len(df2):
        return False, f"Row count mismatch! HTML: {len(df1)}, Parquet: {len(df2)}"

    # Direct content comparison
    if df1.equals(df2):
        return True, "PASS: Data consistency verified for the selected period."
    
    # Generating detailed difference report for debugging
    diff = df1.compare(df2)
    return False, f"Data mismatch found:\n{diff.to_string()}"