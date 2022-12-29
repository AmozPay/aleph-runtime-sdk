#!/usr/bin/python3 -OO

from typing import Any
from custom_plugins import custom_plugins
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(relativeCreated)4f |V %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def maybe_call_plugin(name: str, params: Any):
    plugins = custom_plugins.__dict__
    if plugins[name] is None:
        return
    logger.debug(f"Found plugin '{name}', executing\...")
    plugins[name](params)
    logger.debug(f"Plugin '{name}' exection complete!")
