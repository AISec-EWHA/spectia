import psutil

from common.imports import *
from common.time import *
from common.config import *

proc_util_data = pd.DataFrame(columns=['PID', 'Name', 'CPU Usage (%)', 'Memory Usage (GB)', 'Command'])


class ProcCollector(object):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.proc_util_data_count = self.config_manager.proc_top_n


    @property
    def proc_util_data(self):
        global proc_util_data
        return proc_util_data


    @proc_util_data.setter
    def proc_util_data(self, value):
        global proc_util_data
        proc_util_data = value


    def update_proc_util_data(self, new):
        global proc_util_data
        proc_util_data = new


    @property
    def proc_util(self):
        new_list = []

        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                cpu_usage = proc.info['cpu_percent']
                mem_usage = proc.info['memory_info'].rss / 1024 / 1024 # Convert to MB
                cmd = ' '.join(proc.cmdline())

                new_list.append({
                    'PID': proc.info['pid'],
                    'Name': proc.info['name'],
                    'CPU Usage (%)': cpu_usage,
                    'Memory Usage (GB)': int(mem_usage),
                    'Command': cmd
                })
            except (psutil.ZombieProcess, psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        sorted_list = sorted(new_list, key=lambda x: x['CPU Usage (%)'], reverse=True)[:self.proc_util_data_count] # Sort with CPU
        self.update_proc_util_data(pd.DataFrame(sorted_list))

        return self.proc_util_data
