import streamlit as st
import pandas as pd
import time

from monitoring.gpu import GpuCollector

st.set_page_config(
    page_title="AISEC",
    page_icon="🔐",
)

st.title("Monitoring Dashboard")

st.subheader("GPU")

gpu_usage_data = []
gpu_collector = GpuCollector()
gpu_info = gpu_collector.gpu_info


df = pd.DataFrame(list(gpu_info.items()), columns=['GPU Number', 'Utilization (%)'])
df['Timestamp'] = pd.Timestamp.now()
df.set_index('Timestamp', inplace=True)
gpu_usage_data.append(df)
df_combined = pd.concat(gpu_usage_data)
st.subheader("GPU Usage")
st.area_chart(df_combined.pivot_table(index=df_combined.index, columns='GPU Number', values='Utilization (%)'))