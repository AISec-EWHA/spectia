import os
import pwd
import pynvml
import psutil

from common.imports import *
from common.time import *
from common.config import *


class GpuCollector(object):
    def __init__(self):
        pynvml.nvmlInit()
        self.gpu_num = pynvml.nvmlDeviceGetCount()

        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()

        self.gpu_util_data = pd.DataFrame(columns=['Timestamp', 'GPU', 'Percentage'])
        self.gpu_util_data_count  = self.config_manager.gpu_total_second // self.config_manager.gpu_delta_second
        self.gpu_process_data = pd.DataFrame(columns=['GPU Memory (MB)', 'GPU', 'PID', 'User', 'Command'])
        

    def update_gpu_util_data(self, new):
        self.gpu_util_data = pd.concat([self.gpu_util_data, new], ignore_index=True)

        if len(self.gpu_util_data) // self.gpu_num > self.gpu_util_data_count:
            second = len(self.gpu_util_data) // self.gpu_num - self.gpu_util_data_count
            self.gpu_util_data = self.gpu_util_data.iloc[second*self.gpu_num:]


    def update_gpu_process_data(self, new):
        self.gpu_process_data = new


    @property
    def gpu_util(self):
        new_list = pd.DataFrame(columns=['Timestamp', 'GPU', 'Percentage'])

        timestamp = self.time_manager.get_timestamp

        # Usage of the GPUs
        for i in range(self.gpu_num):
            gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle).gpu

            new = pd.DataFrame([{
                'Timestamp': timestamp,
                'GPU': i,                   # GPU starts from number 0
                'Percentage': gpu_percent
            }])

            new_list = pd.concat([new_list, new], ignore_index=True)
        
        self.update_gpu_util_data(new_list)
        
        return self.gpu_util_data


    @property
    def gpu_process(self):
        new_list = pd.DataFrame(columns=['GPU Memory (MB)', 'GPU', 'PID', 'User', 'Command'])

        # Processes of the GPUs
        for i in range(self.gpu_num):
            gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_processes = pynvml.nvmlDeviceGetComputeRunningProcesses(gpu_handle)

            for process in gpu_processes:
                pid = process.pid
                gpu_memory_usage = process.usedGpuMemory
                process_info = psutil.Process(pid)
                user = process_info.username()
                command = ' '.join(process_info.cmdline())

                new = pd.DataFrame([{
                    'GPU Memory (MB)': gpu_memory_usage / 1024 / 1024,  # Convert to MB
                    'GPU': i,
                    'PID': str(pid),
                    'User': user,
                    'Command': command
                }])

                if not new.empty:
                    new_list = pd.concat([new_list, new], ignore_index=True)

        self.update_gpu_process_data(new_list)
        
        return self.gpu_process_data


    @property
    def color(self):
        return alt.Scale(
            domain=list(range(self.gpu_num)),
            range=[
                '#FF0000', '#FF7F00', '#FFFF00', '#00FF00', 
                '#00FFFF', '#375582', '#7F00FF', '#FF69B4'
            ]
        )


    def __del__(self):
        pynvml.nvmlShutdown()