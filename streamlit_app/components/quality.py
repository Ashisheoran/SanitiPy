import streamlit as st
from utils.ui_helper import severity_badge

def render_quality(issues):
    st.markdown("### Quality Issues")

    if not issues:
        st.success("No issues found")
        return

    for issue in issues:
        st.markdown(f"""
        <div class="issue-row">
            {severity_badge(issue['severity'])}
            <span>{issue['rule']}</span>
            <span>{issue['column']}</span>
        </div>
        """, unsafe_allow_html=True)