import streamlit as st
import time

from common.imports import *
from common.config import *
from monitoring.gpu import GpuCollector
from monitoring.cpu import CpuCollector
from monitoring.mem import MemCollector


st.set_page_config(
    page_title="AISEC",
    page_icon="🔐",
    layout="wide"
)

st.title("Monitoring Dashboard")

config_manager = ConfigManager()
gpu_collector = GpuCollector()
cpu_collector = CpuCollector()
mem_collector = MemCollector()
col1, col2 = st.columns(2)
col1.subheader("GPU Percentage Over Time")
gpu_util_placeholder = col1.empty()
col1.subheader("GPU Usage by Process")
gpu_process_placeholder = col1.empty()
col2.subheader("CPU Percentage by Number")
cpu_util_placeholder = col2.empty()
col2.subheader("Virtual/Swap Memory Usage (GB)")
mem_util_placeholder = col2.empty()

def gpu_util_charts():
    gpu_util_data = gpu_collector.gpu_util
    
    chart = alt.Chart(gpu_util_data).mark_line().encode(
        x=alt.X('Timestamp:O', title='Timestamp', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Percentage:Q', title='Percentage', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(orient='right')),
        color=alt.Color('GPU:N', scale=gpu_collector.color, legend=alt.Legend(orient='left', title='GPU'))
    )

    gpu_util_placeholder.altair_chart(chart, use_container_width=True)


def gpu_process_charts():
    gpu_process_data = gpu_collector.gpu_process
    gpu_process_data = gpu_process_data.sort_values(by='GPU Memory (MB)', ascending=False)

    gpu_process_placeholder.dataframe(gpu_process_data, hide_index=True)


def cpu_util_charts():
    with cpu_util_placeholder.container():
        cols = st.columns(4)
        cpu_util_datas = cpu_collector.cpu_util
        cpu_util_datas = cpu_util_datas.sort_values(by='CPU')

        cpu_util_datas = [
            cpu_util_datas.iloc[i*16:(i+1)*16].reset_index(drop=True)
            for i in range(4)
        ]

        for idx, cpu_data in enumerate(cpu_util_datas):
            chart = alt.Chart(cpu_data).mark_bar().encode(
                x=alt.X('Percentage:Q', title=None, scale=alt.Scale(domain=[0, 100])),
                y=alt.Y('CPU:N', title=None, sort=None),
                color=alt.condition(
                        alt.datum.Percentage >= 50,
                        alt.value('lightsalmon'),
                        alt.value('lightgreen')
                    )
            ).configure_axisY(
                labelAlign='left',
                labelFontSize=12,
                labelOffset=5
            ).configure_view(
                strokeWidth=0
            ).configure_axis(
                grid=False
            )
            
            cols[idx].altair_chart(chart, use_container_width=True)


def mem_util_charts():
    mem_util_data = mem_collector.mem_util

    virtual_chart = alt.Chart(mem_util_data).transform_fold(
        ['Virtual Used', 'Virtual Available'],
        as_=['Category', 'Value']
    ).mark_bar().encode(
        y=alt.Y('Category:N', title=None, sort=None),
        x=alt.X('Value:Q', title=None, scale=alt.Scale(domain=[0, mem_util_data['Virtual Total'].values[0]])),
        color=alt.condition(
            alt.datum.Category == 'Virtual Used',
            alt.value('lightsalmon'),
            alt.value('lightgreen')
        )
    )

    swap_chart = alt.Chart(mem_util_data).transform_fold(
        ['Swap Used', 'Swap Free'],
        as_=['Category', 'Value']
    ).mark_bar().encode(
        y=alt.Y('Category:N', title=None, sort=None),
        x=alt.X('Value:Q', title=None, scale=alt.Scale(domain=[0, mem_util_data['Swap Total'].values[0]])),
        color=alt.condition(
            alt.datum.Category == 'Swap Used',
            alt.value('lightsalmon'),
            alt.value('lightgreen')
        )
    )

    combined_chart = alt.vconcat(virtual_chart, swap_chart)

    mem_util_placeholder.altair_chart(combined_chart, use_container_width=True)


def update_charts():
    gpu_util_charts()
    gpu_process_charts()
    cpu_util_charts()
    mem_util_charts()


while True:
    update_charts()
    time.sleep(config_manager.delta_second)