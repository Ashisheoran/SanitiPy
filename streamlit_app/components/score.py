import streamlit as st
from utils.ui_helper import score_ring_svg

def render_score(score):
    st.markdown("### Quality Score")
    st.markdown(score_ring_svg(score["score"]), unsafe_allow_html=True)