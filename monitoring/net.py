import psutil
import time

from common.imports import *
from common.time import *
from common.config import *

net_util_data = pd.DataFrame(columns=['Timestamp', 'In', 'Out'])


class NetCollector(object):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.time_manager = TimeManager()
        self.net_util_data_count  = self.config_manager.net_total_second // self.config_manager.net_delta_second
        self.net_past = psutil.net_io_counters()
        self.net_delta_second = self.config_manager.net_delta_second

    @property
    def net_util_data(self):
        global net_util_data
        return net_util_data


    @net_util_data.setter
    def net_util_data(self, value):
        global net_util_data
        net_util_data = value


    def update_net_util_data(self, new):
        global net_util_data

        if not self.net_util_data.empty and not new.isna().all().all():
            net_util_data = pd.concat([net_util_data, new], ignore_index=True)

            if len(net_util_data) > self.net_util_data_count:
                net_util_data = net_util_data.iloc[-self.net_util_data_count:]
        else:
            self.net_util_data = new


    @property
    def net_util(self):
        new_list = []

        # Usage of the Inbound/Outbound Traffic
        net_new = psutil.net_io_counters()

        bytes_sent = net_new.bytes_sent - self.net_past.bytes_sent
        bytes_recv = net_new.bytes_recv - self.net_past.bytes_recv

        timestamp = self.time_manager.get_timestamp

        new_list.append({
            'Timestamp': timestamp,
            'Out': round(bytes_sent / 1024 / 1024, 1),    # Convert to MB
            'In': round(bytes_recv / 1024 / 1024, 1),    # Convert to MB
        })

        self.net_past = net_new
        self.update_net_util_data(pd.DataFrame(new_list))
        
        return self.net_util_data