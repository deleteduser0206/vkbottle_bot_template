# -*- coding: utf-8 -*-
"""Модуль с веб-сервером для callback api"""
from aiohttp.web import Request, Response, RouteTableDef

from src.configurator import config
from src.modules import json, logger

routes = RouteTableDef()


@routes.post(path=config.bot.callback.path)
async def confirmation_handler(req: Request):
    """
    Проверяет, что клиент отправил строку,
    которая является {"type": "confirmation"}, то возвращает ему ответ в виде строки,
    её можно получить с помощью запроса к VK API,
    она необходима для подтверждения веб-сервера
    """
    try:
        data = await req.json(loads=json.loads)
        logger.info(data)
    except:  # noqa
        return Response(status=400, text="error")

    if data.get("type") == "confirmation":
        if not config.bot.info.confirmation:
            from src.app import bot

            config.bot.info.confirmation = (
                await bot.api.groups.get_callback_confirmation_code(group_id=data["group_id"])
            ).code
            logger.info(config.bot.info.confirmation)
            return Response(text=config.bot.info.confirmation)

    return Response(status=400, text="error")


@routes.get(path=config.bot.callback.path)
async def route_event_handler(req: Request):
    """Получает событие от пользователя и скармливает его роутеру"""
    try:
        data = await req.json(loads=json.loads)  # noqa
    except:  # noqa
        return Response(status=400, text="error")

    from src.app import bot

    if data.get("secret"):

        async def _():
            if config.bot.callback.secret == data.get("secret"):
                await bot.router.route(event=data, ctx_api=bot.api)
                return Response(text="ok")

            return Response(status=400, text="error")

        if config.bot.callback.secret:
            await _()
        else:
            config.bot.callback.secret = (
                (await bot.api.groups.get_callback_servers(group_id=config.bot.info.group_id))
                .items[0]
                .secret_key
            )
            await _()
    else:
        if config.bot.callback.secret:
            return Response(status=400, text="error")

        await bot.router.route(event=data, ctx_api=bot.api)
        return Response(text="ok")


__all__ = ("routes",)
