import configparser

from common.imports import *


class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.setting = 'default'

    @property
    def get_zone_delta(self):
        return int(self.config.get(self.setting, 'zone_delta'))

    @property
    def get_gpu_total_second(self):
        return int(self.config.get(self.setting, 'gpu_total_second'))

    @property
    def get_gpu_delta_second(self):
        return int(self.config.get(self.setting, 'gpu_delta_second'))