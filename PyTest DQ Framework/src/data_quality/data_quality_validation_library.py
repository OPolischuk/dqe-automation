import pandas as pd

class DataQualityLibrary:
    def check_dataset_is_not_empty(self, df: pd.DataFrame):
        # Verify that the dataset contains at least one row
        assert not df.empty, "DQE Error: The dataset is empty!"

    def check_count(self, source_df: pd.DataFrame, target_df: pd.DataFrame):
        # Compare row counts between source and target
        source_count = len(source_df)
        target_count = len(target_df)
        assert source_count == target_count, \
            f"DQE Error: Row count mismatch! Source: {source_count}, Target: {target_count}"

    def check_data_completeness(self, source_df: pd.DataFrame, target_df: pd.DataFrame):
        # Perform a full content comparison after sorting
        source_sorted = source_df.sort_values(by=list(source_df.columns)).reset_index(drop=True)
        target_sorted = target_df.sort_values(by=list(target_df.columns)).reset_index(drop=True)
        
        # Check if the dataframes are identical
        pd.testing.assert_frame_equal(source_sorted, target_sorted, 
                                      obj="Source vs Target Data Completeness")

    def check_duplicates(self, df: pd.DataFrame):
        # Verify uniqueness of records
        duplicates_count = df.duplicated().sum()
        assert duplicates_count == 0, \
            f"DQE Error: Found {duplicates_count} duplicate rows in the dataset!"

    def check_not_null_values(self, df: pd.DataFrame, columns: list):
        # Validate that specific columns do not contain NULL/NaN values
        for col in columns:
            null_count = df[col].isnull().sum()
            assert null_count == 0, \
                f"DQE Error: Column '{col}' contains {null_count} null values!"