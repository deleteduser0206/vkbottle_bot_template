# -*- coding: utf-8 -*-
"""Модуль для функций, которые выполняются при запуске приложений"""
from asyncio import sleep

from vkbottle import Bot

from src.configurator import config
from src.database.models.db import Base, engine


async def on_startup(bot: Bot):
    """Функция с выполнением задач при запуске бота"""
    await setup_db()

    if config.bot.callback.status:
        config.bot.info.group_id = (await bot.api.groups.get_by_id())[0].id
    else:
        while not bot._polling.group_id:  # noqa
            await sleep(1)
            config.bot.info.group_id = bot._polling.group_id  # noqa


async def setup_db():
    """Очистить базу данных и создать таблицы по описанным моделям"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
