import os
import psutil

from common.imports import *
from common.time import *
from common.config import *


class CpuCollector(object):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()

        self.cpu_util_data = pd.DataFrame(columns=['Timestamp', 'CPU', 'Percentage'])
        
    
    def update_cpu_util_data(self, new):
        self.cpu_util_data = new
    

    @property
    def cpu_util(self):
        new_list = pd.DataFrame(columns=['Timestamp', 'CPU', 'Percentage'])

        timestamp = self.time_manager.get_timestamp

        cpu_percentages = psutil.cpu_percent(percpu=True)

        for i, cpu_percent in enumerate(cpu_percentages):
            new = pd.DataFrame([{
                'Timestamp': timestamp,
                'CPU': i+1,                 # CPU starts from number 1
                'Percentage': cpu_percent
            }])
            
            if not new.empty:
                new_list = pd.concat([new_list, new], ignore_index=True)
        
        self.update_cpu_util_data(new_list)

        return self.cpu_util_data