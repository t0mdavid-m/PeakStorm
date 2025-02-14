from pathlib import Path
import streamlit as st

from src.common.common import page_setup, v_space

page_setup(page="main")

st.markdown("# 👋 Quick Start")
st.markdown("## PeakStorm - from the most intense peak to the full isotope landscape.")
c1, c2 = st.columns(2)
c1.markdown(
    """
    A simple and efficient web application that computes the isotopic envelope of a protein based on the most intense peak. The results can be visualized and downloaded as TSV or Excel for further analysis.

"""
)
v_space(1, c2)
c2.image("assets/pyopenms_transparent_background.png", width=300)
if Path("OpenMS-App.zip").exists():
    st.subheader(
        """
Download the latest version for Windows here by clicking the button below.
"""
    )
    with open("OpenMS-App.zip", "rb") as file:
        st.download_button(
            label="Download for Windows",
            data=file,
            file_name="OpenMS-App.zip",
            mime="archive/zip",
            type="primary",
        )
    st.markdown(
        """
Extract the zip file and run the installer (.msi) file to install the app. The app can then be launched using the corresponding desktop icon.
"""
    )