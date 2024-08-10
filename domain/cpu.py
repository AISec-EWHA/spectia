import psutil
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily


class CpuCollector(object):
    def __init__(self):
        pass

    def collect(self):
        # Number of the CPUs 
        num_cpu_cores = psutil.cpu_count()
        c = CounterMetricFamily("cpu_cores", "Number of CPU Cores", labels=["cpu"])
        c.add_metric(["cores"], num_cpu_cores)
        
        yield c

        # Useage of the CPUs
        cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
        g = GaugeMetricFamily("cpu_usage_percent", "CPU Usage Percentage", labels=["cpu"])
        for i, cpu_percent in enumerate(cpu_percents):
            g.add_metric([f"cpu_{i+1}"], cpu_percent) # CPU number starts at index 1

        yield g