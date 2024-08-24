from datetime import datetime, timedelta, timezone

from common.imports import *
from common.config import *


class TimeManager:
    def __init__(self):
        self.config_manager = ConfigManager()

    @property
    def get_timestamp(self):
        zone = timezone(timedelta(hours=self.config_manager.get_zone_delta))
        zone = datetime.now(zone)
        return zone.strftime('%H:%M:%S')