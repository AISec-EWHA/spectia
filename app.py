import streamlit as st
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx
import time

from common.imports import *
from common.config import *
from monitoring.gpu import GpuCollector
from monitoring.cpu import CpuCollector
from monitoring.mem import MemCollector
from monitoring.disk import DiskCollector
from monitoring.proc import ProcCollector


st.set_page_config(
    page_title="AISEC",
    page_icon="🔐",
    layout="wide"
)

st.title("Monitoring Dashboard")

config_manager = ConfigManager()

if 'gpu_collector' not in st.session_state:
    st.session_state.gpu_collector = GpuCollector()
if 'cpu_collector' not in st.session_state:
    st.session_state.cpu_collector = CpuCollector()
if 'mem_collector' not in st.session_state:
    st.session_state.mem_collector = MemCollector()
if 'disk_collector' not in st.session_state:
    st.session_state.disk_collector = DiskCollector()
if 'proc_collector' not in st.session_state:
    st.session_state.proc_collector = ProcCollector()

gpu_collector = st.session_state.gpu_collector
cpu_collector = st.session_state.cpu_collector
mem_collector = st.session_state.mem_collector
disk_collector = st.session_state.disk_collector
proc_collector = st.session_state.proc_collector

col1, col2 = st.columns(2)
col1.subheader("GPU Percentage Over Time")
gpu_util_placeholder = col1.empty()
col1.subheader("GPU Usage by Process (MB)")
gpu_process_placeholder = col1.empty()
col1.subheader("CPU Usage by Process (MB)")
col1.info(f"📍Shows top {config_manager.proc_top_n} processes only")
proc_util_placeholder = col1.empty()

col2.subheader("CPU Percentage by Number")
cpu_util_placeholder = col2.empty()
col2.subheader("Virtual/Swap Memory Usage (GB)")
mem_util_placeholder = col2.empty()
col2.subheader("Disk Usage by User (GB)")
col2.info(f"📍Update every {int(config_manager.delta_minute / 60)} minutes")
disk_home_placeholder = col2.empty()
col2.subheader("Disk Usage (GB)")
disk_util_placeholder = col2.empty()


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

    if gpu_process_data.empty:
        gpu_process_placeholder.info("🌴No GPU processes are running.")
    else:
        gpu_process_data = gpu_process_data.sort_values(by='GPU Memory', ascending=False)
        gpu_process_placeholder.dataframe(gpu_process_data, hide_index=True, use_container_width=True)


def proc_util_charts():
    proc_util_data = proc_collector.proc_util

    if proc_util_data.empty:
        proc_util_placeholder.info("🌴No CPU processes are running.")
    else:
        proc_util_placeholder.dataframe(proc_util_data, hide_index=True, use_container_width=True)


def cpu_util_charts():
    cpu_count_segment = int(cpu_collector.cpu_count // 4)

    with cpu_util_placeholder.container():
        cols = st.columns(4)
        cpu_util_datas = cpu_collector.cpu_util
        cpu_util_datas = cpu_util_datas.sort_values(by='CPU')

        cpu_util_datas = [
            cpu_util_datas.iloc[i*cpu_count_segment:(i+1)*cpu_count_segment].reset_index(drop=True)
            if i < 3 else cpu_util_datas.iloc[i*cpu_count_segment:].reset_index(drop=True)
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


def disk_util_charts():
    disk_util_data = disk_collector.disk_util
    disk_mount_points = config_manager.disk_mount_points
    disk_util_data = disk_util_data[disk_util_data['Mounted on'].isin(disk_mount_points)]
    disk_util_data = disk_util_data.set_index('Mounted on').reindex(disk_mount_points).reset_index()
    disk_util_placeholder.dataframe(disk_util_data, hide_index=True, use_container_width=True)


def disk_home_charts():
    disk_home_data = disk_collector.disk_home
    disk_home_placeholder.dataframe(disk_home_data, hide_index=True, use_container_width=True)


def update_second_charts():
    gpu_util_charts()
    gpu_process_charts()
    proc_util_charts()
    cpu_util_charts()
    mem_util_charts()
    disk_util_charts()
    

def update_minute_charts():
    while True:
        disk_home_charts()
        time.sleep(config_manager.delta_minute)


minute_thread = Thread(target=update_minute_charts)
add_script_run_ctx(minute_thread)
minute_thread.start()


while True:
    update_second_charts()
    time.sleep(config_manager.delta_second)