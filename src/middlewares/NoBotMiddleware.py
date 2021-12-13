# -*- coding: utf-8 -*-
"""Модуль с middleware который проверяет, что тот, кто отправил команду, не является ботом."""
from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class NoBotMiddleware(BaseMiddleware[Message]):
    """Класс middleware"""

    async def pre(self):
        """Проверяет, что тот, кто отправил команду, не является ботом."""
        if self.event.from_id < 0:
            self.stop("Groups are not allowed to use bot")


__all__ = ("NoBotMiddleware",)
