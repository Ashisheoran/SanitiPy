import streamlit as st
import json

def render_export(profile, issues, score, suggestions):
    st.markdown("### Export Report")

    report = {
        "profile": profile,
        "issues": issues,
        "score": score,
        "suggestions": suggestions
    }

    st.download_button(
        "Download JSON Report",
        data=json.dumps(report, indent=2),
        file_name="sanitify_report.json",
        mime="application/json"
    )