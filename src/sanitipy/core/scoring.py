from __future__ import annotations
from typing import Dict, Any, List

DEFAULT_WEIGHTS = {
    "high_missing": 20,
    "constant_column": 10,
    "high_cardinality": 25,
    "high_duplicate_rate": 30,
}

DEFAULT_CAPS = {
    "high_missing": 40,
    "constant_column": 30,
    "high_cardinality": 40,
    "high_duplicate_rate": 50,
}

class QualityScorer:
    """
    Capped weighted deduction scoring engine.

    - Starts from 100
    - Deducts weighted penalties
    - Caps total penalty per rule
    - Fully explainable output
    """

    def __init__(
            self,
            weights: Dict[str,Any] | None = None,
            caps: Dict[str,Any] | None = None,
    ):
        self.weights = weights or DEFAULT_WEIGHTS
        self.caps = caps or DEFAULT_CAPS

    def score(
            self,
            profile: Dict[str,Any],
            issues: List[Dict[str,Any]]
    ) -> Dict[str,Any]:
        
        base_score = 100
        penalties_by_rule: Dict[str,Any] = {}

        for issue in issues:
            rule = issue['rule']

            weight = self.weights.get(rule,0)
            penalties_by_rule.setdefault(rule,0)
            penalties_by_rule[rule] += weight

        #apply caps
        breakdown = []
        total_penalty = 0

        for rule, raw_penalty in penalties_by_rule.items():
            cap = self.caps.get(rule,raw_penalty)
            applied_penalty = min(raw_penalty,cap)

            breakdown.append({
                "rule": rule,
                "raw_penalty": raw_penalty,
                "applied_penalty": applied_penalty,
                "cap": cap,
            })

            total_penalty += applied_penalty

        final_score = max(base_score - total_penalty, 0)

        return {
            "score": final_score,
            "max_score": base_score,
            "total_penalty": total_penalty,
            "penalties": breakdown,
        }