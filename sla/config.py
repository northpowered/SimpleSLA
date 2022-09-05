import yaml
from pydantic import BaseModel, ValidationError, validator, BaseSettings
from sla.service import Service
from sla.device import Device
from sla.policy import Policy
from sla.logger import LG
import os
import ipaddress

AVAILABLE_SERVICE_TYPES = ["simple-check", "device"]


class DeviceModel(BaseModel):
    name: str
    type: str
    transport: str
    address: str
    username: str
    password: str
    port: int

    def to_sla_device(self) -> dict:
        _: dict = self.dict()
        _.update({'template': f"templates/{self.type}.template"})
        return _


class PolicyModel(BaseModel):
    name: str
    max_rtt: float


class SingleServiceModel(BaseModel):
    name: str
    device: str
    target: str
    delay: int
    policy: str | None


class InGroupService(BaseModel):
    name: str
    target: str
    delay: int
    policy: str | None


class ServiceGroup(BaseModel):
    name: str
    device: str
    services: list[InGroupService]


class BaseSectionModel(BaseModel):

    class Config:
        arbitrary_types_allowed = True
        raw_list = False

    def __repr__(self) -> str:
        return f"<FastAPIConfigurationSection object at {hex(id(self))}>"

    def load(self, section_data: dict | list, section_name: str):

        if self.Config.raw_list:
            section_data = {
                section_name: section_data
            }
        try:
            return self.parse_obj(section_data)
        except KeyError:
            LG.error(f"Missed {section_name} section in config file")
            os._exit(0)
        except ValidationError as ex:
            error = ex.errors()[0]
            LG.error(f"{section_name} | {error.get('loc')[0]} | {error.get('msg')}")  # type: ignore
            os._exit(0)


class ServerSectionModel(BaseSectionModel):
    bind_address: str = "0.0.0.0"
    port: int = 8800
    refresh_time: int = 2

    @validator("port")
    def check_port(cls, v):
        assert isinstance(v, int)
        assert v in range(0, 65535)
        return v

    @validator("bind_address")
    def check_address(cls, v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            assert v == "localhost"
            v = "127.0.0.1"
        return v


class GlobalSectionModel(BaseSectionModel):
    unit: str = "ms"


class LocalSectionModel(BaseSectionModel):
    src_addr: str = "0.0.0.0"
    timeout: int = 1
    ttl: int = 64
    size: int = 56


class DevicesSectionModel(BaseSectionModel):
    class Config:
        raw_list: bool = True
    Devices: list[DeviceModel] | None


class PoliciesSectionModel(BaseSectionModel):
    class Config:
        raw_list: bool = True
    Policies: list[PolicyModel] | None


class ServicesGroupSection(BaseSectionModel):
    class Config:
        raw_list: bool = True
    ServicesGroups: list[ServiceGroup] | None


class ServicesSectionModel(BaseSectionModel):
    class Config:
        raw_list: bool = True
    Services: list[SingleServiceModel] | None


class SLAConfig(BaseSettings):

    def __repr__(self) -> str:
        return f"<SimpleSLAConfiguration object at {hex(id(self))}>"

    Server: ServerSectionModel = ServerSectionModel()
    Global: GlobalSectionModel = GlobalSectionModel()
    Local: LocalSectionModel = LocalSectionModel()
    Devices: DevicesSectionModel = DevicesSectionModel()
    Policies: PoliciesSectionModel = PoliciesSectionModel()
    ServicesGroups: ServicesGroupSection = ServicesGroupSection()
    Services: ServicesSectionModel = ServicesSectionModel()

    def load(self, filename: str):
        raw_data: dict = dict()
        with open(filename, 'r') as f:
            raw_data = yaml.load(f, yaml.loader.SafeLoader)
        self.read_from_dict(raw_data)
        LG.info(f'Configuration was successfully loaded from {filename}')

    def read_from_dict(self, raw_data: dict):
        for section_name in self.__fields__:
            section_data: dict = raw_data.get(section_name, dict())
            section: BaseSectionModel = self.__getattribute__(section_name)
            self.__setattr__(
                section_name,
                section.load(
                    section_data,
                    section_name
                )
            )


config = SLAConfig()
