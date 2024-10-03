import configparser
import ast

from common.imports import *


class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.setting = 'default'

    @property
    def zone_delta(self):
        return int(self.config.get(self.setting, 'zone_delta'))

    @property
    def delta_second(self):
        return int(self.config.get(self.setting, 'delta_second'))

    @property
    def delta_minute(self):
        return int(self.config.get(self.setting, 'delta_minute'))

    @property
    def gpu_total_second(self):
        return int(self.config.get(self.setting, 'gpu_total_second'))

    @property
    def disk_mount_points(self):
        return ast.literal_eval(self.config.get(self.setting, 'disk_mount_points'))

    @property
    def proc_top_n(self):
        return int(self.config.get(self.setting, 'proc_top_n'))