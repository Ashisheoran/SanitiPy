import streamlit as st

from utils.ui_helper import load_css

from components.sidebar import render_sidebar
from components.landing import render_landing
from components.metrics import render_metrics
from components.profile import render_profile
from components.quality import render_quality
from components.score import render_score
from components.fixes import render_fixes
from components.export import render_export

from utils.analysis import run_analysis

st.set_page_config(layout="wide", page_title="Sanitify")

load_css()

df, sample_size, confidence = render_sidebar()

if df is None:
    render_landing()
    st.stop()

profile, issues, score, suggestions = run_analysis(df, sample_size, confidence)

render_metrics(profile, issues, score, suggestions)

tabs = st.tabs(["▣ Profile", "⚠ Issues", "◔ Score", "✦ Fixes", "⤓ Export"])

with tabs[0]:
    render_profile(df, profile)

with tabs[1]:
    render_quality(issues)

with tabs[2]:
    render_score(score)

with tabs[3]:
    render_fixes(df, suggestions)

with tabs[4]:
    render_export(profile, issues, score, suggestions)