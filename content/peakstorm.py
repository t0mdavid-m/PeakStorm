
import streamlit as st
import pyopenms as oms

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.ticker import ScalarFormatter
from src.common.common import page_setup
import pandas as pd
import io

g = oms.CoarseIsotopePatternGenerator()

params = page_setup()

st.title("Calculate Isotopic Envelope")

target = st.number_input("Input most intense peak:", min_value=0.0, value=1000.0)
if st.button('Compute Envelope'):
    with st.spinner('Computing...'):


        start = g.estimateFromPeptideWeight(target).getMostAbundant().getMZ()
        
        uppers = []
        uppers_avg = []
        for delta in np.arange(0, 20, 0.5):
            upper = g.estimateFromPeptideWeight(target+delta).getMostAbundant().getMZ()
            uppers.append(upper)
            uppers_avg.append(target+delta)
            if abs(upper-target) > abs(start-target):
                break

        lowers = []
        lowers_avg = []
        for delta in np.arange(0, 20, 0.5):
            lower = g.estimateFromPeptideWeight(target-delta).getMostAbundant().getMZ()
            lowers.append(lower)
            lowers_avg.append(target-delta)
            if abs(lower-target) > abs(start-target):
                break
        
        sampled_avg = np.array(lowers_avg + [target] + uppers_avg)
        sampled = np.array(lowers + [start] + uppers)

        pos = np.argmin(np.abs(sampled-target))
        best_avg_mass_fit = sampled_avg[pos]
        best_intensity_fit = sampled[pos]

        st.write(f'Most Abundant Mass: {best_intensity_fit} (Δ={best_intensity_fit-target})')

        avg_weight = best_avg_mass_fit

        distribution = g.estimateFromPeptideWeight(avg_weight).getContainer()
        mzs = np.array([p.getMZ() for p in distribution])
        intensities = np.array([p.getIntensity() for p in distribution])

        fig, ax = plt.subplots()
        for mz, intensity in zip(mzs, intensities):
            ax.vlines(x=mz, ymin=0, ymax=intensity, color='black', linewidth=1)

        considered = mzs[intensities > (0.001*max(intensities))]
        ax.set_xlim(np.min(considered), np.max(considered))
        ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=False))
        ax.ticklabel_format(style='plain', axis='x')
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig, use_container_width=False)

        df = pd.DataFrame({
            'mz' : mzs,
            'intensity' : intensities
        })
        df= df[df['intensity'] != 0]

        # Create a TSV file object in memory
        tsv_buffer = io.StringIO()
        df.to_csv(tsv_buffer, sep='\t', index=False)

        # Retrieve the TSV file object
        tsv_buffer.seek(0)
        tsv_file = tsv_buffer.getvalue()
    
        st.download_button(
            label="Download data as CSV", 
            file_name='envelope.tsv', 
            data=tsv_file
        )

    