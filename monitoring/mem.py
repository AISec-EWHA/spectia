import psutil

from common.imports import *
from common.time import *
from common.config import *

class MemCollector(object):
    def __init__(self):
        self.mem_util_data = pd.DataFrame(columns=['Virtual Total', 'Virtual Used', 'Virtual Available', 'Swap Total', 'Swap Used', 'Swap Free'])

        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()

    
    def update_mem_util_data(self, new):
        self.mem_util_data = new


    @property
    def mem_util(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        new = pd.DataFrame([{
            'Virtual Total': mem.total / 1024 / 1024 / 1024, # Convert to GB
            'Virtual Used': mem.used / 1024 / 1024 / 1024,
            'Virtual Available': mem.available / 1024 / 1024 / 1024,
            'Swap Total': swap.total / 1024 / 1024 / 1024, 
            'Swap Used': swap.used / 1024 / 1024 / 1024,
            'Swap Free': swap.free / 1024 / 1024 / 1024,
        }])

        self.update_mem_util_data(new)

        return self.mem_util_data