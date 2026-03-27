# Sanitify

> Intelligent data quality analysis and ML-assisted data cleaning for production Python workflows.

Sanitify is a production-grade Python library built to systematically analyze, validate, score, and improve structured datasets before they enter analytics or machine learning pipelines.

It provides structured profiling, rule-based quality validation, explainable quality scoring, deterministic cleaning utilities, and ML-assisted fix suggestions — all through a single public entry point:

```python
from sanitify import DataCleaner
```

## 🌐 Live Demo [![Live Demo](https://img.shields.io/badge/Live-Demo-red)](https://sanitify.streamlit.app)


You can explore Sanitify through an interactive dashboard:

- 🔗 Live App: https://sanitify.streamlit.app
- 💻 Dashboard Code: https://github.com/Ashisheoran/sanitify-dashboard

The dashboard allows you to:
- Upload datasets
- Analyze data quality
- Apply fixes interactively
- Export reports
 
---

## 🚀 Why Sanitify?

Modern data systems fail more often due to poor data quality than model limitations.

Sanitify helps teams:

- Detect structural issues early
- Quantify dataset health
- Enforce quality standards
- Apply deterministic cleaning safely
- Receive ML-assisted improvement suggestions
- Maintain transparency and reproducibility

Designed for:

- Data Engineers  
- ML Engineers  
- Analytics Teams  
- Data Platform Teams  
- Startups building internal data tooling  

---
 
## 🧠 Design Philosophy

Sanitify follows strict engineering principles:

- **Single public API** — `DataCleaner`
- **No hidden mutations** — data is never altered silently
- **ML never auto-applies fixes** — human-in-the-loop by design
- **Deterministic-first approach** — rules before models
- **Explainable scoring logic**
- **Modular architecture**
- **Production-ready src layout**
- **Test-covered implementation**

---

## 📦 Core Features (v1.0)

- Structured dataset profiling (schema-aware)
- Scalable sampling for large datasets
- Column-level metadata extraction
- Rule-based quality validation engine
- Explainable weighted quality scoring
- Deterministic cleaning operations
- ML-assisted fix suggestions (confidence-based)
- Structured JSON report export
- Clean, modular architecture

---

## ⚙️ Installation

### Development Install

```bash
pip install -e ".[dev]"
```

### Future PyPI Install

```bash
pip install sanitify
```

---

## 🔍 Quick Example

```python
import pandas as pd
from sanitify import DataCleaner

df = pd.read_csv("data.csv")

dc = DataCleaner(df)

# 1. Profile dataset
profile = dc.profile()

# 2. Detect quality issues
issues = dc.check_quality()

# 3. Compute explainable quality score
score = dc.quality_score()

print(score)
```

---

## 📊 Example Output

### Quality Issues

```python
[
  {
    "column": "age",
    "rule": "high_missing",
    "severity": "medium",
    "metric": 0.42,
    "threshold": 0.3
  }
]
```

### Quality Score

```python
{
  "score": 72,
  "max_score": 100,
  "penalties": [
    {"rule": "high_missing", "deduction": 20}
  ]
}
```

Fully transparent. Fully explainable.

---

## 🏗 Architecture Overview

Sanitify uses a modular, production-oriented structure:

```
sanitify/
    datacleaner.py   # Public API
    core/            # Profiling, rules, scoring
    cleaning/        # Deterministic cleaning
    ai/              # ML suggestions
    report/          # Structured exports
    utils/           # Validation & helpers
```

### Architectural Principles

- `src/` layout for clean packaging
- Clear separation of concerns
- Rule engine abstraction
- Configurable scoring engine
- No visualization inside core
- No notebook dependencies
- Stable output schemas

---

## 🧮 Quality Engine

Sanitify includes a rule-based validation system:

Built-in rules (v1):

- High missing rate detection
- Constant column detection
- High cardinality detection
- High duplicate rate detection

The engine is extensible and designed for future plugin support.

---

## 🔐 ML-Assisted Suggestions

Sanitify supports ML-driven fix recommendations.

Key guarantees:

- Suggestions are confidence-scored
- Fixes are never auto-applied
- Users must explicitly approve changes
- Deterministic cleaning remains primary

---

## 🛣 Roadmap

- [x] Structured profiling engine  
- [x] Rule-based validation engine  
- [ ] Weighted scoring engine  
- [ ] Deterministic cleaning utilities  
- [ ] ML suggestion engine  
- [ ] Report exporters (JSON/YAML)  
- [ ] Streamlit demo application  
- [ ] PyPI release  

---

## 🧪 Development

Run tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=sanitify --cov-report=term-missing
```

Sanitify follows:

- Test-driven development
- Modular design
- Public API stability
- Semantic commit conventions

---

## 🤝 Contributing

Contributions are welcome.

Before submitting a PR:

- Ensure tests pass
- Maintain coverage
- Follow existing architecture patterns
- Avoid breaking public API
- Keep changes modular

---

## 📜 License

MIT License

---

## 🔮 Vision

Sanitify aims to become a lightweight but powerful data quality foundation layer for modern Python data stacks — sitting between raw ingestion and analytics/ML pipelines.

Transparent. Deterministic. Extensible. Production-ready.
"# trigger CI" 
