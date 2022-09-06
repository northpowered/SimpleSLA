from .device import Device as SLADevice
from .policy import Policy as SLAPolicy
from threading import Lock
from time import sleep


SERVICE_RESULTS: dict = dict()
SERVICE_STATUSES = {
    "NoData": 0,  # "Black"
    "Normal": 1,  # "Green"
    "Warning": 2,  # "Yellow"
    "Error": 3,  # "Red"
    "OutOfService": 4,  # "Green"
}


class BaseService:
    def __init__(
        self,
        name: str,
        target: str,
        delay: int,
        description: str = str(),
        verbose_name: str = str(),
        policy: SLAPolicy = None,
    ) -> None:
        self.name: str = name
        self.policy: SLAPolicy = policy
        self.target: str = target
        self.delay: int = delay
        self.description: str = description
        self.verbose_name: str = verbose_name

    def _get_status(self, rtt):
        if rtt is False:  # failed to check and recieve rtt
            return SERVICE_STATUSES["NoData"]  # wrong config. Eq to "black"

        if rtt is None and not self.policy:
            return SERVICE_STATUSES[
                "Error"
            ]  # host is unreachable and no policy. Eq to "red"

        if self.policy:
            if rtt is None:
                return SERVICE_STATUSES["Error"]  # Unreachable target. Eq to "red"
            elif self.policy.is_warn(rtt):
                return SERVICE_STATUSES[
                    "Warning"
                ]  # Reachable target, but with overheight rtt. Eq to "yellow"
            else:
                return SERVICE_STATUSES[
                    "Normal"
                ]  # Reachable and rtt<max_rtt. Eq to "green"
        else:
            if isinstance(rtt, (int, float)):
                return SERVICE_STATUSES[
                    "OutOfService"
                ]  # normal, but without policy. Eq to "green"
            else:
                return SERVICE_STATUSES[
                    "NoData"
                ]  # wrong config, but without policy. Eq to "black"

    def get_name(self):
        return self.name


class SubService(BaseService):
    def __init__(
        self,
        name: str,
        target: str,
        delay: int,
        description: str = str(),
        verbose_name: str = str(),
        policy: SLAPolicy = None
    ) -> None:
        super().__init__(name, target, delay, description, verbose_name, policy)


class ServiceGroup:
    def __init__(
        self,
        name: str,
        device: SLADevice,
        services: list[SubService],
        description: str = "",
        verbose_name: str = "",
    ) -> None:
        self.name: str = name
        self.device: SLADevice = device
        self.services: list[SubService] = services
        self.description: str = description
        self.verbose_name: str = verbose_name

    def check(self):
        while True:
            with Lock():
                self.services = self.device.get_rtt(self.services)
                for service in self.services:
                    status = service._get_status(service.__getattribute__('rtt'))
                    _ = {"rtt": service.__getattribute__('rtt'), "status": status}
                    SERVICE_RESULTS[service.name] = _


class Service(BaseService):
    def __init__(
        self,
        name: str,
        target: str,
        delay: int,
        device: SLADevice,
        description: str = str(),
        verbose_name: str = str(),
        policy: SLAPolicy = None,
    ) -> None:
        self.device: SLADevice = device
        super().__init__(name, target, delay, description, verbose_name, policy)

    def check(self):

        while True:
            sleep(self.delay)
            with Lock():
                rtt = self.device.get_rtt(self.target)
                status = self._get_status(rtt)
                _ = {"rtt": rtt, "status": status}
                SERVICE_RESULTS[self.name] = _
