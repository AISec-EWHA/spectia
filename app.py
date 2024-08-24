import streamlit as st
import time

from common.imports import *
from monitoring.gpu import GpuCollector

st.set_page_config(
    page_title="AISEC",
    page_icon="🔐",
)

st.title("Monitoring Dashboard")

gpu_collector = GpuCollector()
gpu_usage_data = []

chart_placeholder = st.empty()

while True:
    df = gpu_collector.gpu_info
    gpu_usage_data.append(df)
    df_combined = pd.concat(gpu_usage_data)
    chart_placeholder.line_chart(df_combined.pivot_table(index=df_combined.index, columns='GPU Number', values='Utilization (%)'))
    time.sleep(1)  # 1초 간격으로 데이터 수집