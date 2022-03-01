from sla.config import SLAConfig
from threading import Thread, Lock
from sla.generator import REGISTRY,Collector
from prometheus_client import start_http_server
from time import sleep
from sla.logger import LG, logger_init
from sla.service import Service


class Sla():
    def __init__(self,config_file:str,log_level:str) -> None:
        logger_init(log_level)
        LG.info("SimpleSLA initialization")
        self.configurator = SLAConfig(config_file=config_file)
        self.threads = list()
        self.active_services = list()

    def start(self):
        self._create_services()
        self._run()

    def _create_services(self):
        services = self.configurator.getServices()
        for key in services.keys():
            thread = Thread(target=services[key].check)
            LG.info(f"Created thread for service {key}")
            self.threads.append(thread)
            thread.start()
            
        REGISTRY.register(Collector())
        LG.info("Services was registered in registry collector")
        _ =  (self.configurator.getBindAddress(), self.configurator.getBindPort())
        start_http_server(_[1],_[0])
        LG.info(f"Prometeus HTTP endpoint started on {_[0]}:{_[1]}")

    def __collect(self):
        _ = self.configurator.getRefreshTime()
        while True:
            with Lock():
                REGISTRY.collect()
                LG.debug(f"Registry collection finished with delay time {_} s")
            sleep(_)

    def _run(self):
        collector_thread = Thread(target=self.__collect)
        collector_thread.start()
        for t in self.threads:
            t.join()
        collector_thread.join()


