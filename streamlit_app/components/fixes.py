import streamlit as st
from sanitify import DataCleaner

def render_fixes(df, suggestions):
    st.markdown("### Suggested Fixes")

    approved = []

    for i, s in enumerate(suggestions):
        st.markdown(f"""
        <div class="sani-card">
            <b>{s['operation']}</b><br>
            Column: {s['column']}<br>
            <small>{s['reason']}</small>
        </div>
        """, unsafe_allow_html=True)

        if st.checkbox("Apply", key=f"fix_{i}"):
            approved.append(s)

    if st.button("Apply Fixes"):
        dc = DataCleaner(df)
        clean_df = dc.apply_fixes(approved)

        st.success("Fixes applied successfully")
        st.dataframe(clean_df, use_container_width=True)