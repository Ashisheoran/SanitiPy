from __future__ import annotations
from typing import Dict, Any, List

class DeterministicSuggestionEngine:
    """
    Generates deteministic fix suggestions based on quality issues and dataset profile metdata.
    """

    def generate(
            self,
            profile: Dict[str, Any],
            issues: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        
        suggestions = []
        seen = set()
        
        for issue in issues:
            rule = issue["rule"]
            column = issue["column"]


            if rule == "high_missing" and column:
                col_meta = profile["columns"][column]
                dtype = col_meta["dtype"]

                if col_meta["missing_pct"] == 1.0:
                    op = "drop_column"
                    reason = "Column is completely missing"
                    confidence = 1.0

                elif "int" in dtype or "float" in dtype:
                    op = "impute_median"
                    reason = "Numeric column with high missing ratio"
                    confidence = 1.0
                else:
                    op = "impute_mode"
                    reason = "Categorical column with high missing ratio"
                    confidence = 1.0

                key = (column, op)
                if key not in seen:
                    suggestions.append({
                        "column": column,
                        "operation": op,
                        "params": {},
                        "confidence": confidence,
                        "reason": reason,
                    })
                    seen.add(key)

            elif rule == "constant_column" and column:
                op = "drop_column"
                reason = "Column has single unique value"
                confidence = 0.9

                key = (column, op)
                if key not in seen:
                    suggestions.append({
                        "column": column,
                        "operation": op,
                        "params": {},
                        "confidence": 0.9,
                        "reason": reason, 
                    })
                    seen.add(key)

            elif rule == "high_cardinality" and column:
                op = "drop_column"
                reason = "Column has high cardinality which may not be useful for modeling"
                confidence = 0.7

                key = (column, op)
                if key not in seen:
                    suggestions.append({
                        "column": column,
                        "operation": op,
                        "params": {},
                        "confidence": confidence,
                        "reason": reason,
                    })
                    seen.add(key)

            elif rule == "high_duplicate_rate":
                op = "drop_duplicates"
                reason = "Dataset has high duplicate rate"
                confidence = 0.8

                key = (column, op)
                if key not in seen:
                    suggestions.append({
                    "column": None,
                    "operation": op,
                    "params": {},
                    "confidence": confidence,
                    "reason": reason,
                })
                seen.add(key)
        return suggestions