from __future__ import annotations
import pandas as pd
from typing import Dict, List, Any

class FixRegistry:
    """
    Registry Mapping Operation name to implementation functions
    """
    @staticmethod
    def drop_column(df: pd.DataFrame, column: str, params: Dict[str,Any]):
        return df.drop(columns=[column])

    @staticmethod
    def impute_mean(df: pd.DataFrame, column: str, params: Dict[str,Any]):
        value = df[column].mean()
        df[column] = df[column].fillna(value)
        return df

    @staticmethod
    def impute_median(df: pd.DataFrame, column: str, params: Dict[str,Any]):
        value = df[column].median()
        df[column] = df[column].fillna(value)
        return df

    @staticmethod
    def impute_mode(df: pd.DataFrame, column: str, params: Dict[str, Any]):
        value = df[column].mode().iloc(0)
        df[column] = df[column].fillna(value)
        return df

    @staticmethod
    def strip_string(df:pd.DataFrame, column: str, params: Dict[str, Any]):
        df[column] = df[column].astype(str).str.strip()
        return df

    @staticmethod
    def drop_duplicate(df: pd.DataFrame, column: str, params: Dict[str, Any]):
        return df.drop_duplicates()

class FixApplier:
    """
    Applies deterministic fixes to a copy of dataframe
    """

    OPERATIONS = {
        "drop_column": FixRegistry.drop_column,
        "impute_mean": FixRegistry.impute_mean,
        "impute_median": FixRegistry.impute_median,
        "impute_mode": FixRegistry.impute_mode,
        "strip_strings": FixRegistry.strip_string,
        "drop_duplicates": FixRegistry.drop_duplicate,
    }

    def apply(
        self,
        df: pd.DataFrame,
        fixes: List[Dict[str, Any]],
    ) -> pd.DataFrame:

        new_df = df.copy()

        for fix in fixes:
            operation = fix["operation"]
            column = fix.get("column")
            params = fix.get("params", {})

            if operation not in self.OPERATIONS:
                raise ValueError(f"Unknown operation: {operation}")

            func = self.OPERATIONS[operation]

            # Dataset-level operations
            if column is None:
                new_df = func(new_df, None, params)
            else:
                if column not in new_df.columns:
                    raise ValueError(f"Column '{column}' not found in dataframe")
                new_df = func(new_df, column, params)

        return new_df

