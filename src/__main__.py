# -*- coding: utf-8 -*-
"""Точка входа для запуска приложений"""
from aiohttp.web import _run_app as run_web  # noqa

from src.app import bot, cb
from src.configurator import config
from src.initialize import on_startup
from src.utils import loop


def main():
    """Функция для запуска задач, приложений"""
    if config.bot.proxy:
        bot.set_proxy(proxy=config.bot.proxy)

    if not config.bot.callback.status:
        bot.loop_wrapper.add_task(bot.run_polling())
    else:
        bot.loop_wrapper.add_task(
            run_web(app=cb, host=config.bot.callback.host, port=config.bot.callback.port)
        )

    bot.loop_wrapper.add_task(on_startup(bot))
    bot.loop_wrapper.run_forever(loop=loop)


if __name__ == "__main__":
    main()
