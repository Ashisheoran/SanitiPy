from pathlib import Path

import streamlit as st


def load_css() -> None:
  css_path = Path(__file__).resolve().parents[1] / "styles.css"
  st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def severity_badge(severity: str) -> str:
    cls = {"high": "badge-high", "medium": "badge-medium", "low": "badge-low"}.get(severity, "badge-low")
    return f'<span class="badge {cls}">{severity.upper()}</span>'


def score_color(score: int) -> str:
    if score >= 80:
        return "#22c55e"
    if score >= 50:
        return "#f59e0b"
    return "#ef4444"


def score_ring_svg(score: int) -> str:
    color = score_color(score)
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
          font-size="32" font-weight="600" fill="{color}">{score}</text>
      </svg>
    </div>
    """