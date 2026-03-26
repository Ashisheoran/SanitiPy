import streamlit as st

def render_landing():

    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center;padding:3rem 0;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:3rem;font-weight:600;
                      color:#f8fafc;letter-spacing:-0.03em;margin-bottom:0.5rem;">
            Saniti<span style="color:#38bdf8">Fy</span>
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