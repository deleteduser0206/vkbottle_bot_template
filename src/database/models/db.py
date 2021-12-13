# -*- coding: utf-8 -*-
"""Модуль с инициализацией базы данных"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.configurator import config
from src.modules import logger
from src.utils import loop

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


async def check_connection():
    """
    Проверка подключения с базой данных,
    если произошла ошибка при попытке подключения,
    в консоль отправляется traceback и скрипт выключается
    """
    async with session as conn:
        try:
            await conn.execute("SELECT 1;")
        except Exception as e:
            logger.exception(e)
            exit()


loop.run_until_complete(check_connection())

__all__ = (
    "Base",
    "engine",
    "session",
)
