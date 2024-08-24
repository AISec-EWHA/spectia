import pynvml

from common.imports import *

class GpuCollector(object):
    def __init__(self):
        pynvml.nvmlInit()

    @property
    def gpu_info(self):
        timestamp = pd.Timestamp.now()

        gpu_usage = []

        # Number of the GPUs
        num_gpu_cores = pynvml.nvmlDeviceGetCount()

        # Usage of the GPUs
        for i in range(num_gpu_cores):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            gpu_usage.append({'GPU Number': i, 'Utilization (%)': gpu_percent, 'Timestamp': timestamp})
        
        df = pd.DataFrame(gpu_usage)
        df.set_index('Timestamp', inplace=True)

        return df

    def __del__(self):
        pynvml.nvmlShutdown()