"""
Sanityfy — Streamlit Dashboard
================================
Demo layer only. Zero business logic lives here.
All analysis is delegated to sanitify.DataCleaner.
"""

from __future__ import annotations

import io
import json
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="SanityFy",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp {
    background-color: #0d0f12;
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #111318 !important;
    border-right: 1px solid #1e2330;
}

[data-testid="stSidebar"] .stMarkdown p {
    color: #64748b;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── Typography ── */
h1, h2, h3 { font-family: 'IBM Plex Mono', monospace !important; }

/* ── Cards ── */
.sani-card {
    background: #111318;
    border: 1px solid #1e2330;
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.sani-card-accent {
    border-left: 3px solid #38bdf8;
}

.sani-card-warn {
    border-left: 3px solid #f59e0b;
}

.sani-card-danger {
    border-left: 3px solid #ef4444;
}

.sani-card-success {
    border-left: 3px solid #22c55e;
}

/* ── Score ring ── */
.score-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 0;
}

.score-ring {
    width: 160px;
    height: 160px;
    position: relative;
}

.score-number {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.8rem;
    font-weight: 600;
    text-align: center;
    line-height: 1;
}

.score-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #475569;
    text-align: center;
    margin-top: 0.4rem;
}

/* ── Metric pill ── */
.metric-row {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}

.metric-pill {
    background: #181c25;
    border: 1px solid #1e2330;
    border-radius: 4px;
    padding: 0.6rem 1rem;
    flex: 1;
    min-width: 110px;
}

.metric-pill .val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.4rem;
    font-weight: 600;
    color: #f8fafc;
}

.metric-pill .lbl {
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-top: 2px;
}

/* ── Issue / suggestion rows ── */
.issue-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid #181c25;
    font-size: 0.88rem;
}

.issue-row:last-child { border-bottom: none; }

.badge {
    display: inline-block;
    padding: 0.15rem 0.55rem;
    border-radius: 3px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.05em;
    font-weight: 500;
    white-space: nowrap;
}

.badge-high   { background: #450a0a; color: #ef4444; }
.badge-medium { background: #431407; color: #f59e0b; }
.badge-low    { background: #052e16; color: #22c55e; }
.badge-rule   { background: #0f172a; color: #38bdf8; border: 1px solid #1e3a5f; }
.badge-op     { background: #1a1025; color: #a855f7; border: 1px solid #2d1b4e; }

.col-name {
    font-family: 'IBM Plex Mono', monospace;
    color: #94a3b8;
    font-size: 0.82rem;
}

/* ── Table overrides ── */
.stDataFrame { font-family: 'IBM Plex Mono', monospace; font-size: 0.82rem; }

[data-testid="stDataFrame"] table {
    border-collapse: collapse;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #1e2330;
    gap: 0;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    color: #475569;
    background: transparent;
    border: none;
    padding: 0.6rem 1.2rem;
}

.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom: 2px solid #38bdf8 !important;
    background: transparent !important;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    border: 1px dashed #1e2330 !important;
    border-radius: 6px;
    background: #111318;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    border-radius: 4px;
    border: 1px solid #1e2330;
    background: #181c25;
    color: #94a3b8;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    border-color: #38bdf8;
    color: #38bdf8;
    background: #0f1929;
}

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: #0c2a3d;
    border-color: #38bdf8;
    color: #38bdf8;
}

/* ── Checkbox ── */
.stCheckbox label { font-size: 0.85rem; color: #94a3b8; }

/* ── Select box ── */
.stSelectbox label { font-size: 0.75rem; color: #475569; letter-spacing: 0.08em; }

/* ── Section headers ── */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #334155;
    border-bottom: 1px solid #1e2330;
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
}

/* ── Logo / wordmark ── */
.wordmark {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    letter-spacing: -0.02em;
}

.wordmark span { color: #38bdf8; }

.version-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #334155;
    letter-spacing: 0.12em;
}

/* ── Progress bar colour ── */
.stProgress > div > div { background-color: #38bdf8 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0d0f12; }
::-webkit-scrollbar-thumb { background: #1e2330; border-radius: 2px; }

/* ── Penalty breakdown bar ── */
.penalty-bar-bg {
    background: #181c25;
    border-radius: 2px;
    height: 6px;
    width: 100%;
    margin-top: 4px;
}
.penalty-bar-fill {
    height: 6px;
    border-radius: 2px;
    background: #ef4444;
}

/* ── Column profile card ── */
.col-profile-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.col-stat {
    background: #0d0f12;
    border-radius: 4px;
    padding: 0.4rem 0.6rem;
}

.col-stat .s-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.95rem;
    font-weight: 500;
    color: #e2e8f0;
}

.col-stat .s-lbl {
    font-size: 0.62rem;
    color: #334155;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _severity_badge(severity: str) -> str:
    cls = {"high": "badge-high", "medium": "badge-medium", "low": "badge-low"}.get(severity, "badge-low")
    return f'<span class="badge {cls}">{severity.upper()}</span>'


def _score_color(score: int) -> str:
    if score >= 80:
        return "#22c55e"
    if score >= 50:
        return "#f59e0b"
    return "#ef4444"


def _score_ring_svg(score: int) -> str:
    color = _score_color(score)
    r = 68
    circ = 2 * 3.14159 * r
    filled = circ * score / 100
    gap = circ - filled
    return f"""
    <div class="score-container">
      <svg width="160" height="160" viewBox="0 0 160 160">
        <circle cx="80" cy="80" r="{r}" fill="none" stroke="#1e2330" stroke-width="10"/>
        <circle cx="80" cy="80" r="{r}" fill="none" stroke="{color}" stroke-width="10"
          stroke-dasharray="{filled:.1f} {gap:.1f}"
          stroke-dashoffset="{circ/4:.1f}"
          stroke-linecap="round"/>
        <text x="80" y="80" text-anchor="middle" dominant-baseline="central"
          font-family="IBM Plex Mono, monospace" font-size="32" font-weight="600"
          fill="{color}">{score}</text>
        <text x="80" y="108" text-anchor="middle"
          font-family="IBM Plex Mono, monospace" font-size="9" letter-spacing="3"
          fill="#475569">/ 100</text>
      </svg>
      <div class="score-label">QUALITY SCORE</div>
    </div>
    """


def _load_sample_dataframes() -> Dict[str, pd.DataFrame]:
    """Built-in sample datasets for instant demo."""
    return {
        "Mixed issues": pd.DataFrame({
            "age":        [25, None, 30, None, 40, None],
            "salary":     [50000, 52000, None, 51000, None, 52000],
            "department": ["HR", "HR", "IT", None, "IT", "IT"],
            "user_id":    ["u1", "u2", "u3", "u4", "u5", "u6"],
            "is_active":  [1, 1, 1, 1, 1, 1],
        }),
        "High cardinality": pd.DataFrame({
            "user_id": [f"user_{i}" for i in range(50)],
            "score":   [i * 1.5 for i in range(50)],
        }),
        "Duplicate rows": pd.DataFrame({
            "A": [1, 2, 3, 1, 2, 3],
            "B": ["x", "y", "z", "x", "y", "z"],
        }),
        "All missing column": pd.DataFrame({
            "name":   ["Alice", "Bob", "Carol", "Dan"],
            "ghost":  [None, None, None, None],
            "salary": [70000, 80000, 75000, 90000],
        }),
        "Clean data": pd.DataFrame({
            "product":  ["A", "B", "C", "D", "E"],
            "revenue":  [100, 200, 150, 300, 250],
            "category": ["X", "Y", "X", "Z", "Y"],
        }),
    }


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="wordmark">Saniti<span>Py</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="version-tag">v1.0.0 · data quality</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<p>Data Source</p>', unsafe_allow_html=True)

    source = st.radio(
        "source",
        ["Upload CSV", "Sample dataset"],
        label_visibility="collapsed",
    )

    df: Optional[pd.DataFrame] = None

    if source == "Upload CSV":
        uploaded = st.file_uploader(
            "Drop a CSV file",
            type=["csv"],
            label_visibility="collapsed",
        )
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                st.success(f"✓  {uploaded.name}")
            except Exception as e:
                st.error(f"Failed to parse: {e}")

    else:
        samples = _load_sample_dataframes()
        chosen = st.selectbox(
            "Choose sample",
            list(samples.keys()),
            label_visibility="collapsed",
        )
        df = samples[chosen]

    if df is not None:
        st.markdown("---")
        st.markdown('<p>Settings</p>', unsafe_allow_html=True)

        sample_size = st.number_input(
            "Max sample size",
            min_value=1_000,
            max_value=500_000,
            value=50_000,
            step=10_000,
        )

        confidence_threshold = st.slider(
            "Suggestion confidence ≥",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05,
            format="%.2f",
        )

    st.markdown("---")
    st.markdown('<p>About</p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#334155;font-size:0.75rem;line-height:1.6">'
        'Sanityfy is a production-grade Python library for intelligent '
        'data quality analysis and ML-assisted cleaning.</p>',
        unsafe_allow_html=True,
    )


# ── Main area ─────────────────────────────────────────────────────────────────

if df is None:
    # ── Landing ──────────────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center;padding:3rem 0;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:3rem;font-weight:600;
                      color:#f8fafc;letter-spacing:-0.03em;margin-bottom:0.5rem;">
            Saniti<span style="color:#38bdf8">Py</span>
          </div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;
                      letter-spacing:0.2em;color:#334155;text-transform:uppercase;
                      margin-bottom:2rem;">
            Intelligent Data Quality · v1.0
          </div>
          <div style="color:#475569;font-size:0.92rem;line-height:1.8;max-width:420px;
                      margin:0 auto 2.5rem;">
            Profile, score, and clean your DataFrames with a single entry point.
            Upload a CSV or pick a sample dataset from the sidebar to begin.
          </div>
          <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;">
            <div class="sani-card" style="width:140px;text-align:center;">
              <div style="font-size:1.4rem;margin-bottom:0.3rem;">⬡</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;
                          letter-spacing:0.1em;color:#38bdf8">PROFILE</div>
              <div style="font-size:0.75rem;color:#475569;margin-top:0.3rem">Structural analysis</div>
            </div>
            <div class="sani-card" style="width:140px;text-align:center;">
              <div style="font-size:1.4rem;margin-bottom:0.3rem;">◈</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;
                          letter-spacing:0.1em;color:#f59e0b">SCORE</div>
              <div style="font-size:0.75rem;color:#475569;margin-top:0.3rem">0–100 quality</div>
            </div>
            <div class="sani-card" style="width:140px;text-align:center;">
              <div style="font-size:1.4rem;margin-bottom:0.3rem;">⟳</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;
                          letter-spacing:0.1em;color:#a855f7">CLEAN</div>
              <div style="font-size:0.75rem;color:#475569;margin-top:0.3rem">Apply & export</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()


# ── Import sanitify once at module level ──────────────────────────────────────
try:
    from sanitify import DataCleaner
except ImportError:
    st.error(
        "**sanitify** is not installed. Run `pip install -e .` from the project root, "
        "then restart Streamlit."
    )
    st.stop()


# ── Run analysis via public API only ─────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _run_analysis(df_json: str, sample_size: int, conf_thresh: float):
    """
    All analysis goes through DataCleaner's locked public API.
    No internal sanitify modules are touched here.
    """
    _df = pd.read_json(io.StringIO(df_json), orient="split")
    dc = DataCleaner(_df)

    profile     = dc.profile(max_sample_size=sample_size)
    issues      = dc.check_quality()
    score       = dc.quality_score()
    suggestions = dc.suggest_fixes(confidence_threshold=conf_thresh)

    return profile, issues, score, suggestions


try:
    with st.spinner("Analysing…"):
        df_json = df.to_json(orient="split")
        profile, issues, score_data, suggestions = _run_analysis(
            df_json, sample_size, confidence_threshold
        )
except Exception as exc:
    st.exception(exc)
    st.stop()


# ── Top metrics bar ───────────────────────────────────────────────────────────
n_rows = profile["dataset"]["rows"]
n_cols = profile["dataset"]["columns"]
n_issues = len(issues)
n_dupes = profile["duplicates"]
score_val = score_data["score"]

st.markdown(f"""
<div class="metric-row">
  <div class="metric-pill">
    <div class="val">{n_rows:,}</div>
    <div class="lbl">Rows</div>
  </div>
  <div class="metric-pill">
    <div class="val">{n_cols}</div>
    <div class="lbl">Columns</div>
  </div>
  <div class="metric-pill">
    <div class="val" style="color:{'#ef4444' if n_issues else '#22c55e'}">{n_issues}</div>
    <div class="lbl">Issues found</div>
  </div>
  <div class="metric-pill">
    <div class="val" style="color:{'#f59e0b' if n_dupes else '#22c55e'}">{n_dupes}</div>
    <div class="lbl">Duplicate rows</div>
  </div>
  <div class="metric-pill">
    <div class="val" style="color:{_score_color(score_val)}">{score_val}</div>
    <div class="lbl">Quality score</div>
  </div>
  <div class="metric-pill">
    <div class="val">{len(suggestions)}</div>
    <div class="lbl">Suggestions</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_profile, tab_quality, tab_score, tab_fix, tab_export = st.tabs([
    "⬡  Profile",
    "◈  Quality Issues",
    "◎  Score",
    "⟳  Fix",
    "↓  Export",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Profile
# ════════════════════════════════════════════════════════════════════════════
with tab_profile:
    st.markdown('<div class="section-header">Dataset overview</div>', unsafe_allow_html=True)

    mem_kb = profile["dataset"]["memory_bytes"] / 1024
    sampled = profile["dataset"]["sampled"]
    sample_n = profile["dataset"]["sample_size"]

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div class="sani-card sani-card-accent">
          <div style="font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;
                      color:#475569;margin-bottom:0.4rem">Memory</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:1.3rem;color:#38bdf8">
            {mem_kb:.1f} KB
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="sani-card sani-card-accent">
          <div style="font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;
                      color:#475569;margin-bottom:0.4rem">Sampling</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:1.3rem;color:#38bdf8">
            {"Yes · " + str(sample_n) if sampled else "No · full"}
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class="sani-card sani-card-accent">
          <div style="font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;
                      color:#475569;margin-bottom:0.4rem">Profile version</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:1.3rem;color:#38bdf8">
            {profile["profile_version"]}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Raw data preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(20), use_container_width=True, height=240)

    st.markdown('<div class="section-header">Column profiles</div>', unsafe_allow_html=True)

    cols_meta = profile["columns"]
    for col_name, meta in cols_meta.items():
        missing_pct = meta["missing_pct"]
        card_cls = "sani-card-danger" if missing_pct > 0.5 else (
            "sani-card-warn" if missing_pct > 0.2 else "sani-card"
        )

        dtype_label = meta["dtype"]
        unique_ratio = meta["unique"] / n_rows if n_rows else 0
        is_constant = meta["is_constant"]

        numeric_html = ""
        if "numeric" in meta and meta["numeric"]["mean"] is not None:
            nm = meta["numeric"]
            numeric_html = f"""
            <div style="margin-top:0.75rem;padding-top:0.75rem;border-top:1px solid #1e2330">
              <div style="font-size:0.62rem;letter-spacing:0.12em;text-transform:uppercase;
                          color:#334155;margin-bottom:0.4rem">Numeric stats</div>
              <div class="col-profile-grid">
                <div class="col-stat"><div class="s-val">{nm['mean']:.2f}</div><div class="s-lbl">mean</div></div>
                <div class="col-stat"><div class="s-val">{nm['median']:.2f}</div><div class="s-lbl">median</div></div>
                <div class="col-stat"><div class="s-val">{nm['std']:.2f}</div><div class="s-lbl">std</div></div>
                <div class="col-stat"><div class="s-val">{nm['min']:.2f}</div><div class="s-lbl">min</div></div>
                <div class="col-stat"><div class="s-val">{nm['max']:.2f}</div><div class="s-lbl">max</div></div>
              </div>
            </div>"""

        flags = ""
        if is_constant:
            flags += '<span class="badge badge-low" style="margin-right:4px">CONSTANT</span>'
        if unique_ratio > 0.9:
            flags += '<span class="badge badge-medium" style="margin-right:4px">HIGH CARDINALITY</span>'
        if missing_pct > 0.3:
            flags += '<span class="badge badge-high" style="margin-right:4px">HIGH MISSING</span>'

        missing_bar = f"""
        <div class="penalty-bar-bg" style="margin-top:4px">
          <div class="penalty-bar-fill" style="width:{missing_pct*100:.1f}%;
            background:{'#ef4444' if missing_pct > 0.5 else '#f59e0b' if missing_pct > 0.2 else '#38bdf8'}">
          </div>
        </div>"""

        st.markdown(f"""
        <div class="sani-card {card_cls}">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
              <span style="font-family:'IBM Plex Mono',monospace;font-weight:600;
                           font-size:0.95rem;color:#f8fafc">{col_name}</span>
              <span style="font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
                           color:#334155;margin-left:0.5rem">{dtype_label}</span>
            </div>
            <div>{flags}</div>
          </div>
          <div class="col-profile-grid" style="margin-top:0.75rem">
            <div class="col-stat">
              <div class="s-val">{meta['missing']}</div>
              <div class="s-lbl">missing</div>
            </div>
            <div class="col-stat">
              <div class="s-val">{missing_pct:.1%}</div>
              <div class="s-lbl">missing %</div>
              {missing_bar}
            </div>
            <div class="col-stat">
              <div class="s-val">{meta['unique']}</div>
              <div class="s-lbl">unique</div>
            </div>
          </div>
          {numeric_html}
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Quality Issues
# ════════════════════════════════════════════════════════════════════════════
with tab_quality:
    st.markdown('<div class="section-header">Detected issues</div>', unsafe_allow_html=True)

    if not issues:
        st.markdown("""
        <div class="sani-card sani-card-success" style="text-align:center;padding:2rem">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:1.1rem;
                      color:#22c55e;margin-bottom:0.4rem">✓ No issues found</div>
          <div style="color:#475569;font-size:0.85rem">Your dataset passed all quality rules.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        rule_counts: Dict[str, int] = {}
        for iss in issues:
            rule_counts[iss["rule"]] = rule_counts.get(iss["rule"], 0) + 1

        # Rule summary pills
        pills_html = "".join(
            f'<div class="metric-pill" style="min-width:90px">'
            f'<div class="val" style="font-size:1.1rem">{cnt}</div>'
            f'<div class="lbl">{rule}</div></div>'
            for rule, cnt in rule_counts.items()
        )
        st.markdown(f'<div class="metric-row">{pills_html}</div>', unsafe_allow_html=True)

        rows_html = ""
        for iss in issues:
            col_label = f'<span class="col-name">{iss["column"]}</span>' if iss["column"] else \
                        '<span class="col-name" style="color:#334155">— dataset level —</span>'
            metric_str = f'{iss["metric"]:.2%}' if isinstance(iss["metric"], float) else str(iss["metric"])
            threshold_str = f'{iss["threshold"]:.2%}' if isinstance(iss.get("threshold"), float) else "—"
            rows_html += f"""
            <div class="issue-row">
              {_severity_badge(iss['severity'])}
              <span class="badge badge-rule">{iss['rule']}</span>
              <div style="flex:1">{col_label}</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#64748b">
                metric: {metric_str} &nbsp;|&nbsp; threshold: {threshold_str}
              </div>
            </div>"""

        st.markdown(f'<div class="sani-card">{rows_html}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Score
# ════════════════════════════════════════════════════════════════════════════
with tab_score:
    col_ring, col_detail = st.columns([1, 2])

    with col_ring:
        st.markdown(_score_ring_svg(score_val), unsafe_allow_html=True)

    with col_detail:
        st.markdown('<div class="section-header">Penalty breakdown</div>', unsafe_allow_html=True)

        if not score_data["penalties"]:
            st.markdown("""
            <div style="color:#22c55e;font-family:'IBM Plex Mono',monospace;
                        font-size:0.88rem;padding:1rem 0">
              No penalties — perfect score.
            </div>
            """, unsafe_allow_html=True)
        else:
            total_penalty = score_data["total_penalty"]
            for pen in score_data["penalties"]:
                bar_w = min(pen["applied_penalty"] / max(total_penalty, 1) * 100, 100)
                cap_hit = pen["applied_penalty"] < pen["raw_penalty"]
                cap_note = f' <span style="color:#334155;font-size:0.7rem">(capped from {pen["raw_penalty"]})</span>' if cap_hit else ""

                st.markdown(f"""
                <div style="margin-bottom:1rem">
                  <div style="display:flex;justify-content:space-between;margin-bottom:2px">
                    <span class="badge badge-rule">{pen['rule']}</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.82rem;
                                 color:#ef4444">−{pen['applied_penalty']}{cap_note}</span>
                  </div>
                  <div class="penalty-bar-bg">
                    <div class="penalty-bar-fill" style="width:{bar_w:.1f}%"></div>
                  </div>
                  <div style="font-size:0.68rem;color:#334155;margin-top:2px">
                    cap: {pen['cap']} pts
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="border-top:1px solid #1e2330;padding-top:1rem;margin-top:0.5rem;
                    display:flex;justify-content:space-between">
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#475569">
            TOTAL PENALTY
          </span>
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.88rem;color:#ef4444;font-weight:600">
            −{score_data['total_penalty']}
          </span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:0.3rem">
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#475569">
            FINAL SCORE
          </span>
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.88rem;
                       color:{_score_color(score_val)};font-weight:600">
            {score_val} / 100
          </span>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Fix
# ════════════════════════════════════════════════════════════════════════════
with tab_fix:
    st.markdown('<div class="section-header">Suggested fixes</div>', unsafe_allow_html=True)

    if not suggestions:
        st.markdown("""
        <div class="sani-card" style="text-align:center;padding:2rem">
          <div style="color:#475569;font-size:0.88rem">
            No suggestions at the current confidence threshold.<br>
            Lower the slider in the sidebar to see more.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        approved_indices = []

        for i, sug in enumerate(suggestions):
            conf_color = "#22c55e" if sug["confidence"] >= 0.85 else (
                "#f59e0b" if sug["confidence"] >= 0.7 else "#ef4444"
            )
            col_label = sug["column"] or "— dataset level —"

            st.markdown(f"""
            <div class="sani-card" style="margin-bottom:0.5rem">
              <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.4rem">
                <span class="badge badge-op">{sug['operation']}</span>
                <span class="col-name">{col_label}</span>
                <div style="flex:1"></div>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
                             color:{conf_color}">
                  {sug['confidence']:.0%} conf.
                </span>
              </div>
              <div style="font-size:0.8rem;color:#475569">{sug['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

            approved = st.checkbox(f"Approve", key=f"fix_{i}", value=True)
            if approved:
                approved_indices.append(i)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("⟳  Apply approved fixes", type="primary"):
            approved_fixes = [suggestions[i] for i in approved_indices]
            if not approved_fixes:
                st.warning("No fixes approved.")
            else:
                try:
                    dc = DataCleaner(df)
                    clean_df = dc.apply_fixes(approved_fixes)

                    st.markdown('<div class="section-header">Cleaned DataFrame preview</div>',
                                unsafe_allow_html=True)

                    col_before, col_after = st.columns(2)
                    with col_before:
                        st.markdown(
                            '<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;'
                            'letter-spacing:0.1em;color:#334155;text-transform:uppercase;'
                            'margin-bottom:0.3rem">Before</div>',
                            unsafe_allow_html=True,
                        )
                        st.dataframe(df, use_container_width=True, height=200)
                        st.caption(f"{df.shape[0]} rows × {df.shape[1]} cols")

                    with col_after:
                        st.markdown(
                            '<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;'
                            'letter-spacing:0.1em;color:#22c55e;text-transform:uppercase;'
                            'margin-bottom:0.3rem">After</div>',
                            unsafe_allow_html=True,
                        )
                        st.dataframe(clean_df, use_container_width=True, height=200)
                        st.caption(f"{clean_df.shape[0]} rows × {clean_df.shape[1]} cols")

                    # Download cleaned CSV
                    csv_bytes = clean_df.to_csv(index=False).encode()
                    st.download_button(
                        "↓  Download cleaned CSV",
                        data=csv_bytes,
                        file_name="cleaned_data.csv",
                        mime="text/csv",
                    )
                    st.session_state["clean_df"] = clean_df

                except Exception as exc:
                    st.exception(exc)


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — Export
# ════════════════════════════════════════════════════════════════════════════
with tab_export:
    st.markdown('<div class="section-header">Export report</div>', unsafe_allow_html=True)

    report = {
        "profile": profile,
        "quality_issues": issues,
        "quality_score": score_data,
        "suggested_fixes": suggestions,
    }

    report_json = json.dumps(report, indent=2)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("""
        <div class="sani-card sani-card-accent">
          <div style="font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;
                      color:#475569;margin-bottom:0.75rem">JSON Report</div>
        """, unsafe_allow_html=True)

        st.download_button(
            "↓  Download report.json",
            data=report_json.encode(),
            file_name="Sanityfy_report.json",
            mime="application/json",
        )

        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("Preview JSON"):
            st.code(report_json[:3000] + ("\n…truncated" if len(report_json) > 3000 else ""),
                    language="json")

    with col_right:
        st.markdown(f"""
        <div class="sani-card">
          <div class="section-header" style="margin-top:0">Report contents</div>
          <div class="issue-row">
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.8rem;
                         color:#38bdf8">profile</span>
            <span style="color:#475569;font-size:0.78rem">{n_cols} columns</span>
          </div>
          <div class="issue-row">
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.8rem;
                         color:#38bdf8">quality_issues</span>
            <span style="color:#475569;font-size:0.78rem">{len(issues)} items</span>
          </div>
          <div class="issue-row">
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.8rem;
                         color:#38bdf8">quality_score</span>
            <span style="color:#475569;font-size:0.78rem">{score_val} / 100</span>
          </div>
          <div class="issue-row">
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.8rem;
                         color:#38bdf8">suggested_fixes</span>
            <span style="color:#475569;font-size:0.78rem">{len(suggestions)} items</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if "clean_df" in st.session_state:
            st.markdown("""
            <div class="sani-card sani-card-success" style="margin-top:1rem">
              <div style="font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;
                          color:#22c55e;margin-bottom:0.4rem">Cleaned DataFrame</div>
              <div style="font-size:0.78rem;color:#475569">Available for download in the Fix tab.</div>
            </div>
            """, unsafe_allow_html=True)