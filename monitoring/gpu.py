import pynvml

from common.imports import *
from common.time import *
from common.config import *


class GpuCollector(object):
    def __init__(self):
        pynvml.nvmlInit()
        self.data = pd.DataFrame(columns=['Timestamp', 'GPU Number', 'Percentage'])
        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()
        self.data_count  = self.config_manager.get_gpu_total_second // self.config_manager.get_gpu_delta_second
        self.gpu_num = pynvml.nvmlDeviceGetCount()


    def update_info(self, new):
        self.data = pd.concat([self.data, new], ignore_index=True)

        if len(self.data) // self.gpu_num > self.data_count:
            second = len(self.data) // self.gpu_num - self.data_count
            self.data = self.data.iloc[second*self.gpu_num:]


    @property
    def get_info(self):
        timestamp = self.time_manager.get_timestamp

        gpu_usage = []

        # Usage of the GPUs
        for i in range(self.gpu_num):
            gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle).gpu
            gpu_new_data = pd.DataFrame([{
                'Timestamp': timestamp,
                'GPU Number': i,
                'Percentage': gpu_percent
            }])

            self.update_info(gpu_new_data)
        
        return self.data


    @property
    def get_color(self):
        return alt.Scale(
            domain=list(range(self.gpu_num)),
            range=[
                '#FF0000', '#FF7F00', '#FFFF00', '#00FF00', 
                '#00FFFF', '#375582', '#7F00FF', '#FF69B4'
            ]
        )


    def __del__(self):
        pynvml.nvmlShutdown()