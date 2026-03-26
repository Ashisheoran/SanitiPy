import streamlit as st

def render_profile(df, profile):
    st.markdown('<div class="section-header">Raw data preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(20), use_container_width=True)

    st.markdown('<div class="section-header">Column profiles</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)

    for i, (col, meta) in enumerate(profile["columns"].items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="sani-card">
                <b>{col}</b><br>
                Missing: {meta['missing_pct']:.2f}<br>
                Unique: {meta['unique']}
            </div>
            """, unsafe_allow_html=True)