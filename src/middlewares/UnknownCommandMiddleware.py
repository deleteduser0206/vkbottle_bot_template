# -*- coding: utf-8 -*-
"""
Модуль с middleware, который после обработки сообщения, проверяет,
что если ни один обработчик не сработал то отправляет пользователю сообщение о том,
что команда не найдена
"""
from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class UnknownCommandMiddleware(BaseMiddleware[Message]):
    """
    Класс с функцией, которая после обработки сообщения, проверяет,
    что если ни один обработчик не сработал то отправляет пользователю сообщение о том,
    что команда не найдена
    """

    async def post(self) -> None:
        """
        Проверка, что если ни один обработчик не сработал,
        то отправляет пользователю сообщение о том,
        что команда не найдена
        """
        if not self.handlers and not self.event.__dict__.get("peer_id") >= 2e9:
            await self.event.answer(
                "Команда не найдена.\nВведите /help для получения списка команд."
            )


__all__ = ("UnknownCommandMiddleware",)
