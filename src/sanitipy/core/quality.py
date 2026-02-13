from __future__ import annotations
from typing import Dict, Any, List


class BaseRule:
    name: str

    def evaluate(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError


class HighMissingRule(BaseRule):
    name = "high_missing"

    def __init__(self, threshold: float = 0.3):
        self.threshold = threshold

    def evaluate(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for col, meta in profile["columns"].items():
            if meta["missing_pct"] > self.threshold:
                results.append({
                    "column": col,
                    "rule": self.name,
                    "severity": "medium",
                    "metric": meta["missing_pct"],
                    "threshold": self.threshold,
                })
        return results


class ConstantColumnRule(BaseRule):
    name = "constant_column"

    def evaluate(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for col, meta in profile["columns"].items():
            if meta["is_constant"]:
                results.append({
                    "column": col,
                    "rule": self.name,
                    "severity": "low",
                    "metric": 1,
                    "threshold": None,
                })
        return results


class HighCardinalityRule(BaseRule):
    name = "high_cardinality"

    def __init__(self, threshold: float = 0.9):
        self.threshold = threshold

    def evaluate(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        rows = profile["dataset"]["rows"]

        if rows == 0:
            return results

        for col, meta in profile["columns"].items():
            ratio = meta["unique"] / rows
            if ratio > self.threshold:
                results.append({
                    "column": col,
                    "rule": self.name,
                    "severity": "medium",
                    "metric": ratio,
                    "threshold": self.threshold,
                })
        return results


class DuplicateRateRule(BaseRule):
    name = "high_duplicate_rate"

    def __init__(self, threshold: float = 0.1):
        self.threshold = threshold

    def evaluate(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        rows = profile["dataset"]["rows"]
        duplicates = profile["duplicates"]

        if rows == 0:
            return []

        rate = duplicates / rows

        if rate > self.threshold:
            return [{
                "column": None,
                "rule": self.name,
                "severity": "high",
                "metric": rate,
                "threshold": self.threshold,
            }]

        return []


class RuleEngine:
    def __init__(self, rules: List[BaseRule]):
        self.rules = rules

    def run(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for rule in self.rules:
            results.extend(rule.evaluate(profile))
        return results
