# -*- coding: utf-8 -*-
import os
import re
from typing import Optional, Union

import yaml

from src.configurator.model import ConfigModel
from src.modules import YamlLoader
from src.modules import logger as project_logger


def get_config(file: str) -> ConfigModel:
    with open(file, "r") as f:
        yaml_config: str = f.read()
        f.close()
        yaml_config: str = remove_comments_from_string(yaml_config)  # type: ignore
        yaml_config: str = replace_value_to_environment(yaml_config)  # type: ignore
        dict_config: dict = yaml.load(yaml_config, YamlLoader)
    config: ConfigModel = ConfigModel(**dict_config)

    if not config.logging.log_console:
        project_logger.remove()

    if config.logging.log:
        enable_file_logging(config.logging.log_path, level=10, logger=project_logger)

    if config.logging.log_errors:
        enable_file_logging(config.logging.log_errors_path, level=30, logger=project_logger)

    return config


FINDALL_VALUES_PATTERN = re.compile(r"\${(\w+)}")
REMOVE_COMMENTS_FROM_STRING_PATTERN = re.compile(r"(?m)^ *#.*\n?")


def remove_comments_from_string(string: str):
    return REMOVE_COMMENTS_FROM_STRING_PATTERN.sub("", string)


def replace_value_to_environment(yaml_config: str) -> str:
    values = FINDALL_VALUES_PATTERN.findall(yaml_config)
    for value in values:
        environ_value: Optional[str] = os.environ.get(value)
        if not environ_value:
            project_logger.error(f"Значение {value} в переменных окружениях пуст.")
            exit(0)
        pattern = rf"\${{{value}}}"
        yaml_config: str = re.sub(  # type: ignore
            pattern=pattern,
            repl=environ_value,
            string=yaml_config,
            count=1,
        )
    return yaml_config


def enable_file_logging(file: str, level: Union[str, int], logger, **kwargs) -> int:
    return logger.add(file, level=level, **kwargs)
