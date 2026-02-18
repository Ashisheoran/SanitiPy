from __future__ import annotations
from typing import Dict, Any, Optional
import json
from pathlib import Path

class ReportBuilder:
    """
    Aggregates all analysis output into a structured report dictionary.
    """
    @staticmethod
    def build(
        profile: Dict[str, Any],
        issues: Any,
        score: Dict[str, Any],
        suggestions: Any,
    ) -> Dict[str, Any]:
        return {
            "profile": profile,
            "quality_issues": issues,
            "quality_score": score,
            "suggested_fixes": suggestions,
        }
    
class BaseExporter:
    """
    Base class for report exporters.
    """
    def export(
            self,
            report: Dict[str, Any],
            path: Optional[str] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError
    
class JSONExporter(BaseExporter):
    """
    Export report to JSON
    """
    def export(
        self,
        report: Dict[str, Any],
        file_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        
        if file_path:
            output_path = Path(file_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4)

        return report