# SanitiPy

SanitiPy is a production-grade Python library for intelligent data quality analysis and ML-assisted data cleaning.

It provides structured dataset profiling, rule-based quality validation, explainable quality scoring, deterministic cleaning utilities, and ML-driven fix suggestions — all through a single public entry point: `DataCleaner`.

SanitiPy is designed for:
- Data engineers
- ML engineers
- Analytics teams
- Production data pipelines

## Key Features (v1.0)

- Structured dataset profiling (schema-aware, scalable sampling)
- Rule-based quality checks
- Explainable quality scoring
- Deterministic cleaning utilities
- ML-assisted fix suggestions (never auto-applied)
- JSON report export

## Philosophy

- No hidden mutations
- No auto-cleaning without approval
- Transparent scoring logic
- Modular architecture
- Production-ready design

## Installation

```bash
pip install sanitipy


(You will update this once published to PyPI.)

---

# ✅ Add Quick Example Section

```markdown
## Quick Example

```python
import pandas as pd
from sanitipy import DataCleaner

df = pd.read_csv("data.csv")

dc = DataCleaner(df)

profile = dc.profile()
issues = dc.check_quality()
score = dc.quality_score()

print(score)


---

# 🎯 Professional Positioning Tip

Do NOT write:

- “This is a beginner project”
- “Learning project”
- “College project”

Position it as a real engineering tool.

---

# 🚀 Optional (Looks More Professional)

Add badges at top of README:

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
