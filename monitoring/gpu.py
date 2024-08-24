import pynvml

from common.imports import *
from common.time import *


class GpuCollector(object):
    def __init__(self):
        pynvml.nvmlInit()
        self.gpu_usage_data = pd.DataFrame(columns=['Timestamp', 'GPU Number', 'Percentage'])
        self.time_manager = TimeManager()


    @property
    def get_info(self):
        timestamp = self.time_manager.get_timestamp

        gpu_usage = []

        # Number of the GPUs
        num_gpu_cores = pynvml.nvmlDeviceGetCount()

        # Usage of the GPUs
        for i in range(num_gpu_cores):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            new_data = pd.DataFrame([{
                'Timestamp': timestamp,
                'GPU Number': i,
                'Percentage': gpu_percent
            }])
            self.gpu_usage_data = pd.concat([self.gpu_usage_data, new_data], ignore_index=True)
        
        return self.gpu_usage_data


    @property
    def get_color(self):
        return alt.Scale(
            domain=list(range(8)),
            range=[
                '#FF0000', '#FF7F00', '#FFFF00', '#7FFF00',
                '#00FF00', '#00FFFF', '#7F00FF', '#FF69B4'
            ]
        )


    def __del__(self):
        pynvml.nvmlShutdown()