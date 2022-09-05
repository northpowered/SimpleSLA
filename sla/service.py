from sla.policy import Policy
from sla.device import Device
from threading import Lock
from time import sleep
from sla.logger import LG
import sys

SERVICE_RESULTS: dict = dict()
SERVICE_STATUSES = {
    "NoData": 0,  # "Black"
    "Normal": 1,  # "Green"
    "Warning": 2,  # "Yellow"
    "Error": 3,  # "Red"
    "OutOfService": 4,  # "Green"
}


class Service:
    def __init__(
        self,
        name: str,
        device: Device,
        target: str,
        delay: int,
        description: str = "",
        verbose_name: str = "",
        policy: Policy = None,
    ) -> None:
        self.name = name
        self.device = device
        self.target = target
        self.delay = delay
        self.description = description
        self.verbose_name = verbose_name
        self.policy = policy

    def get_name(self):
        return self.name

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

    def check(self):

        while True:
            sleep(self.delay)
            with Lock():
                rtt = self.device.get_rtt(self.target)
                status = self._get_status(rtt)
                _ = {"rtt": rtt, "status": status}
                SERVICE_RESULTS[self.name] = _
