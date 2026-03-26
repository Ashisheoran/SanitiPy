import streamlit as st
from utils.ui_helper import score_color

def render_metrics(profile, issues, score, suggestions):
    n_rows = profile["dataset"]["rows"]
    n_cols = profile["dataset"]["columns"]
    n_issues = len(issues)
    n_dupes = profile["duplicates"]
    score_val = score["score"]

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
            <div class="val" style="color:{score_color(score_val)}">{score_val}</div>
            <div class="lbl">Quality score</div>
        </div>
        <div class="metric-pill">
            <div class="val">{len(suggestions)}</div>
            <div class="lbl">Suggestions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)