import configparser

from common.imports import *


class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    @property
    def get_zone_delta(self):
        return int(self.config.get('default', 'zone_delta'))