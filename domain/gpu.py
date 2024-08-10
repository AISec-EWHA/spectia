import pynvml
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class GpuCollector(object):
    def __init__(self):
        pynvml.nvmlInit()

    def collect(self):
        # Number of the GPUs
        num_gpu_cores = pynvml.nvmlDeviceGetCount()
        c = CounterMetricFamily("gpu_cores", "Number of GPU Cores", labels=["gpu"])
        c.add_metric(["cores"], num_gpu_cores)
        
        yield c

        # Usage of the GPUs
        g = GaugeMetricFamily("gpu_usage_percent", "GPU Usage Percentage", labels=["gpu"])
        for i in range(num_gpu_cores):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_percent = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            g.add_metric([f"gpu_{i}"], gpu_percent) # GPU number starts at index 0

        yield g

    def __del__(self):
        pynvml.nvmlShutdown()
        