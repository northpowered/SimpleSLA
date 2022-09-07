from time import sleep
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
    BaseConnection,
    ReadTimeout
)
import textfsm
from sla.logger import LG
from ping3 import ping
from sla.tracer import device_tracer
from pydantic import BaseModel
from sla import SLAConfig


class DeviceMapping(BaseModel):
    devices: list[str] = ["m716", "cisco", "juniper", "eltex", "potok-km-122"]

    @staticmethod
    def get_rtt_command(type: str, target: str) -> str | None:
        commands: dict = {
            "m716": f"ping -c 1 {target}",
            "cisco": f"ping {target} repeat 1",
            "juniper": f"ping {target} count 1",
            "eltex": f"ping {target} detailed packets 1",
            "potok-km-122": f"ping {target} count 1",
        }
        return commands.get(type, None)

    @staticmethod
    def get_connection_type(type: str, transport: str) -> str | None:
        connections: dict = {
            "m716": {"ssh": "generic"},
            "cisco": {"telnet": "cisco_ios_telnet", "ssh": "cisco_ios"},
            "juniper": {"telnet": "juniper_junos_telnet", "ssh": "juniper_junos"},
            "eltex": {"ssh": "eltex"},
            "potok-km-122": {"ssh": "generic"},
        }
        return connections.get(type, dict()).get(transport, None)


class Device:
    def __init__(self, **parameters) -> None:
        self.name = parameters["name"]
        self.type = parameters["type"]
        self.transport = parameters.get("transport", None)
        self.address = parameters.get("address", None)
        self.username = parameters.get("username", None)
        self.password = parameters.get("password", None)
        self.port = parameters.get("port")
        self.template = parameters.get("template", None)

    def __create_remote_connection(self) -> BaseConnection | None:
        device_type: str = DeviceMapping().get_connection_type(self.type, self.transport)
        if not device_type:
            LG.warning(
                f"Unsupported transport {self.transport} for self.type device type"
            )
            return None  # NoData status for service
        connection: dict = {
            "device_type": device_type,
            "host": self.address,
            "username": self.username,
            "password": self.password,
            "port": self.port,
        }
        return ConnectHandler(**connection)

    def __create_rtt_command(self, target: str) -> str | None:
        command: str = DeviceMapping().get_rtt_command(self.type, target)
        if not command:
            LG.warning(
                f"Unknown device type {self.type}"
            )
            return None  # NoData status for service
        return command

    def __get_rtt_remote(self, hnd: BaseConnection, target: str, fsm: textfsm.TextFSM):
        _ = None
        command: str = self.__create_rtt_command(target)
        result = hnd.send_command(command)
        LG.debug(f"RTT command sent to {self.name} device")
        output = fsm.ParseText(result)
        try:
            _ = float(output[0][0])
        except IndexError as ex:
            _ = None
        except Exception as ex:
            _ = False
        finally:
            return _

    def __batch_remote_check(self, hnd: BaseConnection, targets: list, fsm: textfsm.TextFSM) -> dict:
        iter: int = 0
        for target in targets:
            sleep(target.delay)
            _ = None
            command: str = self.__create_rtt_command(target.target)
            try:
                result = hnd.send_command(command)
            except ReadTimeout:
                LG.debug(f"ReadTimeout error on {self.name} device for {target.target} target")
                continue  # Ignore ReadTimeout error and continue checking
            LG.debug(f"Command [{command}] sent to {self.name} device")
            LG.debug(f"Recieved [{result}] from {self.name} device")
            output = fsm.ParseText(result)
            LG.debug(f"Parsed data [{output}] from {self.name} device")
            try:
                rtt = float(output[iter][0])
            except IndexError as ex:
                rtt = None
            except Exception as ex:
                rtt = False
            target.__setattr__('rtt', rtt)
            iter = iter + 1
        return targets

    def __get_rtt_local(self, target: str):
        _ = None
        try:
            _ = ping(
                target,
                timeout=SLAConfig.Local.timeout,
                unit=SLAConfig.Global.unit,
                src_addr=SLAConfig.Local.src_addr,
                ttl=SLAConfig.Local.ttl,
                size=SLAConfig.Local.timeout
            )
        except UnicodeError:
            LG.error(f"Wrong Ipv4 syntax: {target}")
        except OSError as error:
            LG.error(f"Source interface/address {error} is not exist")
        else:
            pass
        finally:
            return _

    def get_rtt(self, target: str | list) -> str | dict:
        with device_tracer.start_as_current_span(__name__) as span:
            span.set_attribute("device.type", self.type)
            rtt = None
            if self.type == "local":
                rtt = self.__get_rtt_local(target)
            elif self.type in DeviceMapping().devices:
                try:
                    connection: BaseConnection = self.__create_remote_connection()
                    LG.debug(f"Connected to {self.name} device")
                    with open(self.template, "r") as template:
                        fsm = textfsm.TextFSM(template)
                        if isinstance(target, str):
                            rtt = self.__get_rtt_remote(connection, target, fsm)
                        else:
                            rtt = self.__batch_remote_check(connection, target, fsm)
                except FileNotFoundError:
                    LG.error(f"Template file {self.template} not found")
                except NetmikoTimeoutException:
                    LG.warning(f"Unreachable device. Connection with {self.name} failed")
                except NetmikoAuthenticationException as error:
                    LG.warning(f"Authentication with {self.name} failed. Check credentials")
            else:
                LG.error(f"Unknown device type {self.type}")
            return rtt
