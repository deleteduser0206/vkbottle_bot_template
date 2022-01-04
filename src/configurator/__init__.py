# -*- coding: utf-8 -*-
from pathlib import Path

from src.configurator.model import ConfigModel
from src.configurator.utils import get_config, get_config_from_file

config_path = str(
    Path(Path(__file__).parent, "..", "..", "config.yml").absolute()
)  # ./../../config.yml
config: ConfigModel = get_config_from_file(config_path)

__all__ = (
    "ConfigModel",
    "config",
    "get_config",
)
