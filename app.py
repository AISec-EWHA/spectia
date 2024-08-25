import streamlit as st
import time

from common.imports import *
from common.config import *
from monitoring.gpu import GpuCollector


st.set_page_config(
    page_title="AISEC",
    page_icon="🔐",
)

st.title("Monitoring Dashboard")

config_manager = ConfigManager()
gpu_collector = GpuCollector()
gpu_placeholder = st.empty()


def gpu_charts():
    gpu_data = gpu_collector.get_info
    
    chart = alt.Chart(gpu_data).mark_line().encode(
        x=alt.X('Timestamp:O', title='Timestamp', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Percentage:Q', title='Percentage', scale=alt.Scale(domain=[0, 100])),
        color=alt.Color('GPU Number:N', scale=gpu_collector.get_color)
    ).properties(
        title='GPU Usage'
    )

    gpu_placeholder.altair_chart(chart, use_container_width=True)


while True:
    gpu_charts()
    time.sleep(config_manager.delta_second)