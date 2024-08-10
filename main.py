import time

import configparser
from domain.cpu import CpuCollector
from domain.gpu import GpuCollector
from domain.mem import MemoryCollector
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY


def register():
    REGISTRY.register(CpuCollector())
    REGISTRY.register(GpuCollector())
    REGISTRY.register(MemoryCollector())


def server(): # Start Exporter server 
    config = configparser.ConfigParser()
    config.read('./config.ini')
    port = config.getint('default', 'port')
    start_http_server(port)
    print(f"Spectia server is started in port {port}.")


if __name__ == '__main__':
    register()
    server()

    while True:
        time.sleep(1)