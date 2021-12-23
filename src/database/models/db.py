# -*- coding: utf-8 -*-
"""Модуль с инициализацией базы данных"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.configurator import config

if not config.database.url:
    config.database.url = (
        f"{config.database.dialect}{f'+{config.database.driver}' if config.database.driver else ''}://"  # noqa
        f"{config.database.user}:{config.database.password}@"
        f"{'' if config.database.unix_socket else f'{config.database.host}:{config.database.port}'}"  # noqa
        f"/"
        f"{config.database.database}"
        f"?"
        f"autocommit=true"
        f"&host={config.database.unix_socket or ''}"
    )
    "Dialect[+driver]://User[password]@[host]:[port]/database?autocommit=true[&host=unix_socket]"

engine = create_async_engine(config.database.url)
Base = declarative_base(bind=engine)
session = AsyncSession(bind=engine)

__all__ = (
    "Base",
    "engine",
    "session",
)
