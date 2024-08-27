import psutil

from common.imports import *
from common.time import *
from common.config import *

class DiskCollector(object):
    def __init__(self):
        self.disk_util_data = pd.DataFrame(columns=['Mounted on', 'Size', 'Used', 'Avail', 'Percentage'])

        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()

    
    def update_disk_util_data(self, new):
        self.disk_util_data = new


    @property
    def disk_util(self):
        new_list = []

        partitions = psutil.disk_partitions()

        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)

            new_list.append({
                'Mounted on': partition.mountpoint,
                'Size': usage.total / 1024 / 1024 / 1024,  # Convert to GB
                'Used': usage.used / 1024 / 1024 / 1024,
                'Avail': usage.free / 1024 / 1024 / 1024,
                'Percentage': usage.percent
            })

        self.update_disk_util_data(pd.DataFrame(new_list))

        return self.disk_util_data