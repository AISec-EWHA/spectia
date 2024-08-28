import os
import psutil
import subprocess

from common.imports import *
from common.time import *
from common.config import *

disk_util_data = pd.DataFrame(columns=['Mounted on', 'Size', 'Used', 'Avail', 'Percentage'])
disk_home_data = pd.DataFrame(columns=['User', 'Usage'])


class DiskCollector(object):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()

    
    @property
    def disk_util_data(self):
        global disk_util_data
        return disk_util_data


    @disk_util_data.setter
    def disk_util_data(self, value):
        global disk_util_data
        disk_util_data = value


    @property
    def disk_home_data(self):
        global disk_home_data
        return disk_home_data


    @disk_home_data.setter
    def disk_home_data(self, value):
        global disk_home_data
        disk_home_data = value

    
    def update_disk_util_data(self, new):
        global disk_util_data
        disk_util_data = new

    
    def update_disk_home_data(self, new):
        global disk_home_data
        disk_home_data = new


    @property
    def disk_util(self):
        new_list = []

        partitions = psutil.disk_partitions()

        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)

            new_list.append({
                'Mounted on': partition.mountpoint,
                'Size': int(usage.total / 1024 / 1024 / 1024),  # Convert to GB
                'Used': int(usage.used / 1024 / 1024 / 1024),
                'Avail': int(usage.free / 1024 / 1024 / 1024),
                'Percentage': usage.percent
            })

        self.update_disk_util_data(pd.DataFrame(new_list))

        return self.disk_util_data


    @property
    def disk_home(self):
        new_list = []

        subdirs = [os.path.join('/home', d.name) for d in os.scandir('/home') if d.is_dir()]


        for sudir in subdirs:
            result = subprocess.run(['du', '-sh', sudir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            new_list.append({
                'User': str(sudir.split('/')[-1]),
                'Usage': str(result.stdout.decode('utf-8').split()[0])
            })

        self.update_disk_home_data(pd.DataFrame(new_list))

        return self.disk_home_data