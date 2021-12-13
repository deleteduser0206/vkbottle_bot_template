# -*- coding: utf-8 -*-
"""Сборка приложений"""
from aiohttp.web import Application

from src.blueprints import bps
from src.bot import Bot
from src.configurator import config
from src.custom.StateDispenser import StateDispenser
from src.middlewares import mws
from src.utils import loop, loop_wrapper
from src.web.callback import routes

bot: Bot = (
    Bot(
        token=config.bot.token,
        state_dispenser=StateDispenser(),
        loop=loop,
        loop_wrapper=loop_wrapper,
    )
    .add_blueprint(blueprint=bps)
    .add_middleware(middleware=mws)
)

cb = Application()
cb.add_routes(routes=routes)

__all__ = (
    "bot",
    "cb",
)
