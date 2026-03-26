import streamlit as st
import pandas as pd
from typing import Optional, Dict

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="wordmark">Saniti<span>Fy</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="version-tag">v1.0.0 · data quality</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


        source = st.radio(
            "source",
            ["Upload CSV", "Sample Dataset"],
            horizontal=True,
        )

        df: Optional[pd.DataFrame] = None 
        sample_size = 50_000
        confidence_threshold = 0.0

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
            'SanitiPy is a production-grade Python library for intelligent '
            'data quality analysis and ML-assisted cleaning.</p>',
            unsafe_allow_html=True,
        )

    return df, sample_size, confidence_threshold


# Creating a sample dataframe

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