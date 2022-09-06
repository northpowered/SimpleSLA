from threading import Thread, Lock
from sla import (
    SLADevice,
    SLAService,
    SLAServiceGroup,
    SLAConfig,
    SLAPolicy,
    SLASubService
)
from sla.generator import REGISTRY, Collector
from prometheus_client import start_http_server
from time import sleep
from sla.logger import LG, logger_init


class Sla:
    def __init__(self, config_file: str, log_level: str, log_dest: str) -> None:
        logger_init(log_level, log_dest)
        LG.info("SimpleSLA initialization")
        self.threads: list = list()
        self.active_services: list = list()
        self.services: dict = dict()
        self.service_groups: dict = dict()
        self.devices: dict = dict()
        self.policies: dict = dict()

    def _load_devices(self):
        if SLAConfig.Policies.Policies:
            for device in SLAConfig.Devices.Devices:
                self.devices.update(
                    {
                        device.name: SLADevice(
                            **device.to_sla_device()
                        )
                    }
                )
        self.devices.update(
            {
                'simplesla-local': SLADevice(
                    name="simplesla-local",
                    type="local",
                )
            }
        )

    def _load_policies(self):
        if not SLAConfig.Policies.Policies:
            return
        for policy in SLAConfig.Policies.Policies:
            self.policies.update(
                {
                    policy.name: SLAPolicy(
                        name=policy.name,
                        max_rtt=policy.max_rtt
                    )
                }
            )

    def _load_services(self):
        if not SLAConfig.Services.Services:
            return
        for service in SLAConfig.Services.Services:
            self.services.update(
                {
                    service.name: SLAService(
                        name=service.name,
                        target=service.target,
                        delay=service.delay,
                        description='foobar',
                        verbose_name='foobar',
                        device=self.devices.get(service.device),
                        policy=self.policies.get(service.policy)
                    )
                }
            )

    def _load_service_groups(self):
        if not SLAConfig.ServicesGroups.ServicesGroups:
            return
        for service_group in SLAConfig.ServicesGroups.ServicesGroups:
            sub_services: list[SLASubService] = list()
            for sub in service_group.services:
                if not sub.delay:
                    sub.delay = service_group.delay
                if not sub.policy:
                    sub.policy = service_group.policy
                sub_services.append(
                    SLASubService(
                        name=sub.name,
                        target=sub.target,
                        delay=sub.delay,
                        description=str(),
                        verbose_name=str(),
                        policy=self.policies.get(sub.policy)
                    )
                )
            self.service_groups.update(
                {
                    service_group.name: SLAServiceGroup(
                        name=service_group.name,
                        device=self.devices.get(service_group.device),
                        description='foobar',
                        verbose_name='foobar',
                        services=sub_services
                    )
                }
            )

    def start(self):
        self._load_devices()
        self._load_policies()
        self._load_services()
        self._load_service_groups()
        self._create_services()
        self._run()

    def _create_services(self):
        for key in self.services.keys():
            thread = Thread(target=self.services[key].check)
            LG.info(f"Created thread for service {key}")
            self.threads.append(thread)
            thread.start()

        for key in self.service_groups.keys():
            thread = Thread(target=self.service_groups[key].check)
            LG.info(f"Created thread for service group {key}")
            self.threads.append(thread)
            thread.start()

        REGISTRY.register(Collector())
        LG.info("Services was registered in registry collector")
        _ = (SLAConfig.Server.bind_address, SLAConfig.Server.port)
        start_http_server(_[1], _[0])
        LG.info(f"Prometeus HTTP endpoint started on {_[0]}:{_[1]}")

    def __collect(self):
        _ = SLAConfig.Server.refresh_time
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
