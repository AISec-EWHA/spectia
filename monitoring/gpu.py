import os
import pwd
import pynvml
import psutil

from common.imports import *
from common.time import *
from common.config import *

gpu_util_data = pd.DataFrame(columns=['Timestamp', 'GPU', 'Percentage'])
gpu_process_data = pd.DataFrame(columns=['GPU Memory', 'GPU', 'PID', 'User', 'Command'])


class GpuCollector(object):
    def __init__(self):
        pynvml.nvmlInit()
        self.gpu_num = pynvml.nvmlDeviceGetCount()

        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()
        self.gpu_util_data_count  = self.config_manager.gpu_total_second // self.config_manager.delta_second

   
    @property
    def gpu_util_data(self):
        global gpu_util_data
        return gpu_util_data


    @gpu_util_data.setter
    def gpu_util_data(self, value):
        global gpu_util_data
        gpu_util_data = value


    @property
    def gpu_process_data(self):
        global gpu_process_data
        return gpu_process_data


    @gpu_process_data.setter
    def gpu_process_data(self, value):
        global gpu_process_data
        gpu_process_data = value


    def update_gpu_util_data(self, new):
        global gpu_util_data
        gpu_util_data = pd.concat([gpu_util_data, new], ignore_index=True)

        if len(gpu_util_data) // self.gpu_num > self.gpu_util_data_count:
            gpu_util_data = gpu_util_data.iloc[-self.gpu_num*self.gpu_util_data_count:]


    def update_gpu_process_data(self, new):
        global gpu_process_data
        gpu_process_data = new


    @property
    def gpu_util(self):
        new_list = []

        timestamp = self.time_manager.get_timestamp

        # Usage of the GPUs
        for i in range(self.gpu_num):
            gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle).gpu

            new_list.append({
                'Timestamp': timestamp,
                'GPU': i,                   # GPU starts from number 0
                'Percentage': gpu_percent
            })
        
        self.update_gpu_util_data(pd.DataFrame(new_list))
        
        return self.gpu_util_data


    @property
    def gpu_process(self):
        new_list = []

        # Processes of the GPUs
        for i in range(self.gpu_num):
            gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_processes = pynvml.nvmlDeviceGetComputeRunningProcesses(gpu_handle)

            for process in gpu_processes:
                try:
                    pid = process.pid
                    gpu_memory_usage = process.usedGpuMemory
                    process_info = psutil.Process(pid)
                    user = process_info.username()
                    command = ' '.join(process_info.cmdline())

                    new_list.append({
                        'GPU Memory': gpu_memory_usage / 1024 / 1024,  # Convert to MB
                        'GPU': i,
                        'PID': str(pid),
                        'User': user,
                        'Command': command
                    })
                except (psutil.ZombieProcess, psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        self.update_gpu_process_data(pd.DataFrame(new_list))
        
        return self.gpu_process_data


    @property
    def color(self):
        colors = [
                '#FF0000', '#FF7F00', '#FFFF00', '#00FF00', 
                '#00FFFF', '#375582', '#7F00FF', '#FF69B4'
            ]

        if self.gpu_num > len(colors):
            rand_colors = [
                '#{:06X}'.format(random.randint(0, 0xFFFFFF))
                for _ in range(self.gpu_num - len(base_colors))
            ]
            colors = colors + rand_colors

        return alt.Scale(
            domain=list(range(self.gpu_num)),
            range=colors
        )


    def __del__(self):
        pynvml.nvmlShutdown()