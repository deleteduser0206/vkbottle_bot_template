# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel


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


class ConfigModel(BaseModel):
    bot: _Bot
    database: _Database
    logging: _Logging
