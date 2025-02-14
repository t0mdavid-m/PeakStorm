import streamlit as st
from pathlib import Path

if __name__ == '__main__':
    pages = {
        "PeakStorm" : [
            st.Page(Path("content", "quickstart.py"), title="Quickstart", icon="👋"),
            st.Page(Path("content", "peakstorm.py"), title="Isotopic Envelope Calculator", icon="📶"),
        ]
    }

    pg = st.navigation(pages)
    pg.run()