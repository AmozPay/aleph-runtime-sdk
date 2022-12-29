#!/usr/bin/python3 -OO

from typing import Dict, Optional, List
import os
from dataclasses import dataclass, field
from plugin_exec import maybe_call_plugin
from runtime_types import ConfigurationPayload, Volume, Encoding, Interface, NetworkPluginParameters


def get_dns_servers():
    return ["1.1.1.1"]

def get_volumes():
    return [Volume(**{
    "mount": "/mnt/path",
    "device": "sda1-fake",
    "read_only": True
})]

def get_variables():
    return {
    "OS": "Linux",
    "NODE_ENV": "dev",
    "REACT_VARIABLE": "hello world"
}

@dataclass
class ConfigurationPayload:
    code: bytes = b"foobar"
    encoding: Encoding = "plain"
    entrypoint: str = "./fake_entrypoint.sh"
    input_data: bytes = b"barfoo"
    interface: Interface = "exectutable"
    vm_hash: str = "fakehash"
    ip: Optional[str] = "127.0.0.1"
    route: Optional[str] = "/route/path"
    dns_servers: List[str] = field(default_factory=get_dns_servers)
    volumes: List[Volume] = field(default_factory=get_volumes)
    variables: Optional[Dict[str, str]] = field(default_factory=get_variables)

def setup_hostname(hostname: str):
    maybe_call_plugin("before_hostname", hostname)
    os.environ["ALEPH_ADDRESS_TO_USE"] = hostname
    print(f"Dummy call: hostname {hostname}")
    maybe_call_plugin("after_hostname", hostname)

def setup_variables(variables: Optional[Dict[str, str]]):
    maybe_call_plugin("before_variables", variables)
    if variables is None:
        return
    for key, value in variables.items():
        os.environ[key] = value
    maybe_call_plugin("after_variables", variables)

def setup_volumes(volumes: List[Volume]):
    maybe_call_plugin("before_volumes", volumes)
    for volume in volumes:
        print(f"Mounting /dev/{volume.device} on {volume.mount}")
        print(f"Dummy call: mkdir -p {volume.mount}")
        if volume.read_only:
            print(f"Dummy call: mount -t squashfs -o ro /dev/{volume.device} {volume.mount}")
        else:
            print(f"Dummy call: mount -o rw /dev/{volume.device} {volume.mount}")
    maybe_call_plugin("after_volumes", volumes)
    print("Dummy call: mount")

def setup_network(
    ip: Optional[str], route: Optional[str], dns_servers: Optional[List[str]] = None
):
    network_params = NetworkPluginParameters(**{
        "ip": ip,
        "route": route,
        "dns_servers": dns_servers
    })
    maybe_call_plugin("before_network", network_params)
    print("Fake network setup")
    maybe_call_plugin("after_network", network_params)

def setup_system(config: ConfigurationPayload):
    maybe_call_plugin("before_system", config)

    setup_hostname(config.vm_hash)
    setup_variables(config.variables)
    setup_volumes(config.volumes)
    setup_network(config.ip, config.route, config.dns_servers)

    maybe_call_plugin("after_system", config)
    print("Setup finished")

if __name__ == "__main__":
    config = ConfigurationPayload()
    setup_system(config)
