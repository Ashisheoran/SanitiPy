import pandas as pd
import io
from sanitify import DataCleaner

def run_analysis(df, sample_size, confidence):
    dc = DataCleaner(df)

    profile = dc.profile(max_sample_size=sample_size)
    issues = dc.check_quality()
    score = dc.quality_score()
    suggestions = dc.suggest_fixes(confidence_threshold=confidence)

    return profile, issues, score, suggestions