import os
import psutil

from common.imports import *
from common.time import *
from common.config import *

cpu_util_data = pd.DataFrame(columns=['Timestamp', 'CPU', 'Percentage'])


class CpuCollector(object):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()
        
    @property
    def cpu_util_data(self):
        global cpu_util_data
        return cpu_util_data


    @cpu_util_data.setter
    def cpu_util_data(self, value):
        global cpu_util_data
        cpu_util_data = value

    
    def update_cpu_util_data(self, new):
        global cpu_util_data
        cpu_util_data = new
    

    @property
    def cpu_util(self):
        new_list = []

        timestamp = self.time_manager.get_timestamp

        cpu_percentages = psutil.cpu_percent(percpu=True)

        for i, cpu_percent in enumerate(cpu_percentages):
            new_list.append({
                'Timestamp': timestamp,
                'CPU': i+1,                 # CPU starts from number 1
                'Percentage': cpu_percent
            })
        
        self.update_cpu_util_data(pd.DataFrame(new_list))

        return self.cpu_util_data