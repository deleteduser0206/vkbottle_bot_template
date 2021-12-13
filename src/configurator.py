# -*- coding: utf-8 -*-
"""Модуль с взаимодействиями над конфигурацией"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from os import environ
from pathlib import Path
from re import findall, sub
from typing import Any, List, Optional, Union

import yaml
from pydantic import BaseModel

from src.modules import YamlLoader, json, logger


class _Callback(BaseModel):
    status: bool = False
    host: str = "0.0.0.0"
    port: int = 8080
    path: str = "/"
    secret: Optional[str] = ""


class _Info(BaseModel):
    group_id: int = 0
    confirmation: str = ""


class _Bot(BaseModel):
    token: Union[List[str], str]
    admins: List[int] = []
    proxy: Optional[str] = None
    callback: _Callback
    info: _Info = _Info()


class _Redis(BaseModel):
    cache: bool = False
    host: str = "127.0.0.1"
    port: int = 6342
    user: Optional[str] = None
    password: Optional[str] = None
    database: int = 0
    unix_socket: Optional[str] = None
    url: Optional[str] = None
    time_to_del: int = 86400


class _Database(BaseModel):
    host: str = "127.0.0.1"
    port: int = 3306
    user: Optional[str] = None
    password: Optional[str] = None
    database: str = "vkbottle_bot_template"
    dialect: str = "mysql"
    driver: str = "aiomysql"
    fix_auto_increment: bool = False
    unix_socket: Optional[str] = None
    url: Optional[str] = None
    redis: _Redis


class _Logging(BaseModel):
    log: bool = False
    log_errors: bool = False
    log_console: bool = True
    log_path: str = "logs/%Y-%M-%d_%H-%M-%S.log"
    log_errors_path: str = "logs/%Y-%M-%d_%H-%M-%S-error.log"


class _Environment(BaseModel):
    status: bool = False
    translate: Any


class ConfigModel(BaseModel):
    bot: _Bot
    database: _Database
    logging: _Logging
    environment: _Environment


# fmt: off
handler_id_console = logger._core.handlers[0]._id  # type: ignore # noqa
# fmt: on


def disable_console_logging(handler_id):
    """Удаляет logger по его handler id"""
    logger.remove(handler_id)


def update_dict(dict_, replaceable) -> dict:
    """Обновление значений вложенного словаря разной глубины"""
    # Источник: https://bit.ly/3ED24FI

    for key, val in replaceable.items():  # noqa
        if isinstance(val, Mapping):
            dict_[key] = update_dict(dict_.get(key, {}), val)
        else:
            dict_[key] = val
    return dict_


def replace_env_to_config(config_) -> dict:
    """Функция для подстановки значений из виртуального окружения в конфиг"""
    replace_dict = config_["environment"]
    replaceable_dict = config_

    cfg = json.dumps(replace_dict["translate"]).decode()
    for key, val in set(findall(r"\"(\w+)\":\"(\w+)\"", cfg)):  # for string
        env_val = environ.get(val, "null")
        if env_val == "null":
            cfg = sub(f'"{key}":"{val}"', f'"{key}":{env_val}', cfg)
        else:
            cfg = sub(f'"{key}":"{val}"', f'"{key}":"{env_val}"', cfg)
    for key, val in set(findall(r"\"(\w+)\":(\w+)", cfg)):  # for integer
        env_val = environ.get(val, "null")
        if env_val == "null":
            cfg = sub(f'"{key}":"{val}"', f'"{key}":{env_val}', cfg)
        else:
            cfg = sub(f'"{key}":"{val}"', f'"{key}":"{env_val}"', cfg)

    return update_dict(replaceable_dict, json.loads(cfg))


def get_abs_path(file: str, name_config_file: str):
    """Получить путь к файлу конфигурации"""
    script_path = Path(file).parent.absolute()

    base_path = Path(script_path, name_config_file)
    back_path = Path(script_path, "..", name_config_file)

    if base_path.exists():
        return base_path.absolute()

    if back_path.exists():
        return back_path.absolute()

    logger.error(f"Файл {base_path} или {back_path} не найдены. Они созданы?")
    exit()


def enable_file_logging(file: str, level: Union[str, int], *args, **kwargs) -> int:
    """Активирует дублирование текста из консоли, в файл"""
    file_ = Path(file)
    if file_.parents[0].is_dir() and file_.parents[0].exists():
        return logger.add(datetime.now().strftime(file), level=level, *args, **kwargs)
    elif file_.parents[1].is_dir() and file_.parents[1].exists():
        return logger.add(
            Path(
                file.split("/")[0], "/", datetime.now().strftime(Path(file).name).__str__()
            ).__str__(),
            level=level,
            *args,
            **kwargs,
        )
    else:
        logger.error("Не удалось создать файл логов")

    return -1


def make_config(file: str) -> ConfigModel:
    """Получить конфигурацию из {file}.yml"""
    with open(get_abs_path(__file__, file), mode="r", encoding="utf-8") as file_:
        config_ = yaml.load(file_.read(), YamlLoader)
        config_ = ConfigModel(**config_)
        file_.close()

    if config_.environment.status is True:
        config_ = ConfigModel(**replace_env_to_config(config_.__dict__))

    if config_.logging.log:
        enable_file_logging(file=config_.logging.log_path, level=10)  # Logging.DEBUG

    if config_.logging.log_errors:
        enable_file_logging(file=config_.logging.log_errors_path, level=40)  # Logging.ERROR

    if config_.logging.log_console is False:
        disable_console_logging(handler_id_console)

    return config_


config: ConfigModel = make_config("../config.yml")

__all__ = (
    "config",
    "ConfigModel",
)
