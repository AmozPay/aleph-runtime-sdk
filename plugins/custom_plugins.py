#!/usr/bin/python3 -OO


from typing import Dict
from runtime_types import Plugins
import os

def react_variables_plugin(vars: Dict[str, str]):
    keys_to_change = []
    for key, value in vars.items():
        if key.startswith("REACT_"):
            keys_to_change.append((key, value))
    for key, value in keys_to_change:
        vars.pop(key)
        key = key.replace("REACT_", "")
        vars[key] = value

def colored_print(txt: str):
    print(f"\033[2;31m{txt}\033[0;0m")

def print_environment(vars: Dict[str, str]):
    print("printing the environment variable Dict:")
    print(vars)
    print("\nNow printing os.environ")
    for key, value in dict(os.environ).items():
        if key in vars.keys():
            colored_print(f"{key}={value}")
        else:
            print(f"{key}={value}")

custom_plugins = Plugins(
    before_variables=react_variables_plugin,
    after_variables=print_environment
)
