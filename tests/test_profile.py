import pandas as pd
from sanitipy import DataCleaner


def test_missing_percentage():

    df = pd.DataFrame({"A": [1, None, None, 4]})
    profile = DataCleaner(df).profile()

    assert profile["columns"]["A"]["missing"] == 2
    assert profile["columns"]["A"]["missing_pct"] == 0.5

def test_unique_count():

    df = pd.DataFrame({"A": [1, 1, 2, 2]})
    profile = DataCleaner(df).profile()

    assert profile["columns"]["A"]["unique"] == 2

def test_numeric_all_null():

    df = pd.DataFrame({"A": [None, None]})
    profile = DataCleaner(df).profile()

    numeric = profile["columns"]["A"]["numeric"]
    assert numeric["mean"] is None

def test_duplicates():

    df = pd.DataFrame({"A": [1, 1], "B": [2, 2]})
    profile = DataCleaner(df).profile()

    assert profile["duplicates"] == 1

def test_no_sampling():

    df = pd.DataFrame({"A": [1, 2, 3]})
    profile = DataCleaner(df).profile(max_sample_size=100)

    assert profile["dataset"]["sampled"] is False
    assert profile["dataset"]["sample_size"] == 3

def test_high_missing_rule():
    df = pd.DataFrame({"A":[1,None,None,None]})
    results = DataCleaner(df).check_quality()

    assert any(r["rule"] == "high_missing" for r in results)

def test_quality_score_basic():
    df = pd.DataFrame({
        "A": [None, None, None, None],    # high missing
        "B": [1,1,1,1],                 #constant
    })

    dc = DataCleaner(df)
    score = dc.quality_score()

    assert score["score"] < 100
    assert score["total_penalty"] > 0
    assert "penalties" in score

def test_apply_fixes_impute():
    df = pd.DataFrame({"A": [1, None, 3]})
    dc = DataCleaner(df)

    fixes = [{"column": "A", "operation": "impute_mean"}]
    clean_df = dc.apply_fixes(fixes)

    assert clean_df["A"].isna().sum() == 0
    assert df["A"].isna().sum() == 1 

def test_drop_column():
    df = pd.DataFrame({"A":[1,2], "B": [3,4]})
    dc = DataCleaner(df)

    fixes = [{"column": "A", "operation": "drop_column"}]
    clean_df = dc.apply_fixes(fixes)

    assert "A" not in clean_df.columns
    assert "A" in df.columns

def test_drop_duplicates():

    df = pd.DataFrame({"A": [1, 1, 2]})
    dc = DataCleaner(df)

    fixes = [{"column": None, "operation": "drop_duplicates"}]
    clean_df = dc.apply_fixes(fixes)

    assert len(clean_df) == 2
    assert len(df) == 3

def test_strip_strings():

    df = pd.DataFrame({"A": [" x ", " y "]})
    dc = DataCleaner(df)

    fixes = [{"column": "A", "operation": "strip_strings"}]
    clean_df = dc.apply_fixes(fixes)

    assert clean_df["A"].tolist() == ["x", "y"]

import pytest
def test_unknown_operation():

    df = pd.DataFrame({"A": [1, 2]})
    dc = DataCleaner(df)

    fixes = [{"column": "A", "operation": "unknown_op"}]

    with pytest.raises(ValueError):
        dc.apply_fixes(fixes)

def test_suggest_fixes_numeric_missing():
    df = pd.DataFrame({"A": [1, None, None]})
    dc = DataCleaner(df)

    suggestions = dc.suggest_fixes()

    assert any(s["operation"] == "impute_median" for s in suggestions)

def test_suggest_full_missing_column():

    df = pd.DataFrame({"A": [None, None, None]})
    dc = DataCleaner(df)

    suggestions = dc.suggest_fixes()

    assert any(s["operation"] == "drop_column" for s in suggestions)
    assert not any(s["operation"] == "impute_mode" for s in suggestions)

def test_suggest_high_cardinality():

    df = pd.DataFrame({
        "user_id": [f"user_{i}" for i in range(50)]
    })

    dc = DataCleaner(df)
    suggestions = dc.suggest_fixes()

    assert any(s["operation"] == "drop_column" for s in suggestions)

def test_suggestion_deduplication():

    df = pd.DataFrame({"A": [None, None, None]})
    dc = DataCleaner(df)

    suggestions = dc.suggest_fixes()

    drop_ops = [s for s in suggestions if s["operation"] == "drop_column"]
    assert len(drop_ops) == 1

def test_export_report_returns_dict(tmp_path):
    df = pd.DataFrame({"A": [1, None, 4]})
    dc = DataCleaner(df)

    report = dc.export_report()

    assert "profile" in report
    assert "quality_issues" in report
    assert "quality_score" in report
    assert "suggested_fixes" in report

def test_export_report_writes_file(tmp_path):
    df = pd.DataFrame({"A": [1, None, 4]})
    dc = DataCleaner(df)

    output_file = tmp_path / "report.json"
    dc.export_report(path= str(output_file))

    assert output_file.exists()