from __future__ import annotations
import pandas as pd
from typing import Any, Dict, List, Optional

from sanitipy.core.profiler import DataProfiler
from sanitipy.core.quality import (
    RuleEngine,
    HighCardinalityRule,
    HighMissingRule,
    ConstantColumnRule,
    DuplicateRateRule,
)

class DataCleaner:
    """
    Public entry point for SanitiPy.
    Stable API surface. Avoid breaking changes.
    """
    
    def __init__(self,df:pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("DataCleaner expects a pandas DataFrame")
        
        self._df = df.copy()
        self._profile_cache: Optional[Dict[str,Any]] = None

    # ------Profilling------
    def profile(self, max_sample_size: int = 50_000):
        profiler = DataProfiler(self._df, max_sample_size=max_sample_size)

        self._profile_cache = profiler.run()
        return self._profile_cache
    
    # ------Quality------
    def check_quality(self):
        if self._profile_cache is None:
            self.profile()
        
        rules = [
            HighMissingRule(),
            HighCardinalityRule(),
            ConstantColumnRule(),
            DuplicateRateRule(),
        ]

        engine = RuleEngine(rules)
        return engine.run(self._profile_cache)
    
    def quality_score(self):
        raise NotImplementedError
    
    # ------ML Suggestions------
    def suggest_fixes(self, confidene_threshold: float = 0.8):
        raise NotImplementedError
    
    # ------Apply------
    def apply_fixes(self, approved):
        raise NotImplementedError
    
    # ------Reporting------
    def export_report(self, format: str = "json"):
        raise NotImplementedError