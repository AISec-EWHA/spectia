import psutil
from prometheus_client.core import GaugeMetricFamily

class MemoryCollector(object):
    def __init__(self):
        pass

    def collect(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Usage of memory
        m_g = GaugeMetricFamily("memory_usage_bytes", "Memory Usage Statistics", labels=["mem"])
        m_g.add_metric(["total"], mem.total)
        m_g.add_metric(["available"], mem.available)
        m_g.add_metric(["used"], mem.used)
        m_g.add_metric(["free"], mem.free)
        
        yield m_g

        # Usage of Swap memory
        s_g = GaugeMetricFamily("swap_usage_bytes", "Swap Usage Statistics", labels=["mem"])
        s_g.add_metric(["total"], swap.total)
        s_g.add_metric(["used"], swap.used)
        s_g.add_metric(["free"], swap.free)
        
        yield s_g
