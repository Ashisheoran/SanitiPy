from __future__ import annotations
import pandas as pd
import numpy as np 
from typing import Dict, Any, Tuple

class DataProfiler:
    """
    Deterministic dataset profiler.

    Design principles:
    - Sampling only affects heavy numeric computations.
    - Structural metrics (missing, unique, duplicates) use full dataset.
    - Output is stable and versioned.
    - No side effects.
    """

    PROFILE_VERSION = "1.0"

    def __init__(self,df:pd.DataFrame, max_sample_size: int = 50_000):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("DataProfiler expects a pandas DataFrame")
        
        self._original_df = df
        self._max_sample_size = max_sample_size
        self._df, self._sampled = self._apply_sampling(df)

    # ------------------------
    # Public API
    # ------------------------
    def run(self) -> Dict[str,Any]:
        return{
            "profile_version": self.PROFILE_VERSION,
            "dataset": self._dataset_summary(),
            "columns": self._column_profiles(),
            "duplicates": self._duplicates_count(),
        }
    
    # ------------------------
    # Dataset Level
    # ------------------------
    def _dataset_summary(self) -> Dict[str,Any]:
        return {
            "rows": int(self._original_df.shape[0]),
            "cols": int(self._original_df.shape[1]),
            "memory_bytes": int(self._original_df.memory_usage(deep=True).sum()),
            "sampled": self._sampled,
            "sample_size": int(len(self._df)),
        }
    
    def _duplicates_count(self) -> int:
        return int(self._df.duplicated().sum())
    
    # ------------------------
    # Column Level
    # ------------------------
    def _column_profiles(self) -> Dict[str,Any]:
        profiles: Dict[str,Any] = {}

        total_rows = len(self._original_df)

        for col in self._original_df.columns:
            full_series = self._original_df[col]
            # sampled series not required for the current metrics; keep using full_series

            col_profile = self._base_column_metrics(
                full_series,
                total_rows                
                )

            if self._is_numeric(full_series) or full_series.dropna().empty:
                col_profile['numeric'] = self._numeric_metrics(full_series)
            
            profiles[col] = col_profile

        return profiles
    
    def _base_column_metrics(self, series: pd.Series, total_rows: int) -> Dict[str,Any]:
        missing = series.isna().sum()
        unique = series.nunique(dropna=True)

        return {
            "dtype": str(series.dtype),
            "missing": int(missing),
            "missing_pct": float(missing / total_rows) if total_rows > 0 else 0.0,
            "unique": int(unique),
            "is_constant": bool(unique <= 1),
        }
    
    def _numeric_metrics(self, series: pd.Series) -> Dict[str,Any]:
        clean = series.dropna()
        
        if clean.empty:
            return {
                "mean": None,
                "std": None,
                "min": None,
                "max": None,
                "median": None,
            }
        return {
            "mean": float(clean.mean()),
            "std": float(clean.std()),
            "min": float(clean.min()),
            "max": float(clean.max()),
            "median": float(clean.median()),
        }

    # ------------------------
    # sampling
    # ------------------------
    def _apply_sampling(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, bool]:

        if len(df) > self._max_sample_size:
            return (
                df.sample(
                n=self._max_sample_size,
                random_state=42
                )
            ), True
        
        return df, False
    
    #------------------------
    # type checks
    #------------------------
    @staticmethod
    def _is_numeric(series: pd.Series) -> bool:
        return pd.api.types.is_numeric_dtype(series)
    