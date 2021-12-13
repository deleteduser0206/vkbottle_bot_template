# -*- coding: utf-8 -*-
"""Модуль с инициализацией redis базы данных"""
from aioredis import Redis

from src.configurator import config
from src.utils import loop


async def connect():
    """Функция подключения и получения реализации протокола redis"""
    kwargs = dict(
        username=config.database.redis.user,
        password=config.database.redis.password,
        db=config.database.redis.database,
        decode_responses=True,
        retry_on_timeout=True,
    )
    if config.database.redis.unix_socket:
        redis_connection = await Redis(
            unix_socket_path=config.database.redis.unix_socket,
            **kwargs,
        )
    else:
        redis_connection = await Redis(
            host=config.database.redis.host,
            port=config.database.redis.port,
            **kwargs,
        )

    return redis_connection


redis: Redis = loop.run_until_complete(connect()) if config.database.redis.cache else None
__all__ = ("redis",)
