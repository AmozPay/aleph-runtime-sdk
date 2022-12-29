#!/usr/bin/python3 -OO

from enum import Enum
from dataclasses import dataclass, field
from typing import (
    Optional,
    Dict,
    Any,
    List,
    NewType,
    Any,
    List,
    NewType,
    Callable,
    Optional,
    Dict
)


ASGIApplication = NewType("AsgiApplication", Any)

class Encoding(str, Enum):
    plain = "plain"
    zip = "zip"
    squashfs = "squashfs"


class Interface(str, Enum):
    asgi = "asgi"
    executable = "executable"


class ShutdownException(Exception):
    pass


@dataclass
class Volume:
    mount: str
    device: str
    read_only: bool

@dataclass
class ConfigurationPayload:
    code: bytes
    encoding: Encoding
    entrypoint: str
    input_data: bytes
    interface: Interface
    vm_hash: str
    ip: Optional[str] = None
    route: Optional[str] = None
    dns_servers: List[str] = field(default_factory=list)
    volumes: List[Volume] = field(default_factory=list)
    variables: Optional[Dict[str, str]] = None


@dataclass
class RunCodePayload:
    scope: Dict

@dataclass
class NetworkPluginParameters:
    ip: Optional[str]
    route: Optional[str]
    dns_servers: Optional[List[str]]

VariablesPlugin = Callable[[Dict[str, str]], Any]
HostnamePlugin = Callable[[str], Any]
VolumesPlugin = Callable[[List[Volume]], Any]
NetworkPlugin = Callable[[NetworkPluginParameters], Any]
SystemPlugin = Callable[[ConfigurationPayload], Any]

@dataclass
class Plugins:
    before_volumes: Optional[VolumesPlugin]
    after_volumes: Optional[VolumesPlugin]
    before_system: Optional[SystemPlugin]
    after_system: Optional[SystemPlugin]
    before_variables: Optional[VariablesPlugin]
    after_variables: Optional[VariablesPlugin]
    before_hostname: Optional[HostnamePlugin]
    after_hostname: Optional[HostnamePlugin]
    before_network: Optional[NetworkPlugin]
    after_network: Optional[NetworkPlugin]

    def __init__(
        self,
        before_system: Optional[SystemPlugin] = None,
        before_volumes: Optional[VolumesPlugin] = None,
        before_variables: Optional[VariablesPlugin] = None,
        after_volumes: Optional[VolumesPlugin] = None,
        after_system: Optional[SystemPlugin] = None,
        after_variables: Optional[VariablesPlugin] = None,
        before_hostname: Optional[HostnamePlugin] = None,
        after_hostname: Optional[HostnamePlugin] = None,
        before_network: Optional[NetworkPlugin] = None,
        after_network: Optional[NetworkPlugin] = None,
    ):
        self.before_volumes = before_volumes
        self.before_system = before_system
        self.before_variables = before_variables
        self.before_network = before_network
        self.before_hostname = before_hostname

        self.after_volumes = after_volumes
        self.after_system = after_system
        self.after_variables = after_variables
        self.after_network = after_network
        self.after_hostname = after_hostname
