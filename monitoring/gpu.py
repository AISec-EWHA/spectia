import pynvml

class GpuCollector(object):
    def __init__(self):
        pynvml.nvmlInit()

    @property
    def gpu_info(self):
        gpu_usage = {}

        # Number of the GPUs
        num_gpu_cores = pynvml.nvmlDeviceGetCount()

        # Usage of the GPUs
        for i in range(num_gpu_cores):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            gpu_usage[i] = gpu_percent
        
        return gpu_usage

    def __del__(self):
        pynvml.nvmlShutdown()