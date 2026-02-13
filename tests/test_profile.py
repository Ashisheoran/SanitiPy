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