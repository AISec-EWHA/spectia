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
gpu_util_placeholder = st.empty()
gpu_process_placeholder = st.empty()


def gpu_util_charts():
    gpu_util_data = gpu_collector.gpu_util
    
    chart = alt.Chart(gpu_util_data).mark_line().encode(
        x=alt.X('Timestamp:O', title='Timestamp', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Percentage:Q', title='Percentage', scale=alt.Scale(domain=[0, 100])),
        color=alt.Color('GPU:N', scale=gpu_collector.color)
    ).properties(
        title='GPU Usage'
    )

    gpu_util_placeholder.altair_chart(chart, use_container_width=True)


def gpu_process_charts():
    gpu_process_data = gpu_collector.gpu_process
    gpu_process_data = gpu_process_data.sort_values(by='GPU Memory (MB)', ascending=False)

    gpu_process_placeholder.dataframe(gpu_process_data, hide_index=True)


while True:
    gpu_util_charts()
    gpu_process_charts()
    time.sleep(config_manager.delta_second)