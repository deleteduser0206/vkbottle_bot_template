# -*- coding: utf-8 -*-
from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class PrepareCommandMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        """
        Замена/добавление знаков в тексте для обработчиков,
        что бы не заполнять массив ненужными значениями с командами
        """
        if self.event.text.startswith("!"):
            self.event.text = self.event.text.replace("!", "/", 1)

        if not self.event.text.startswith(("!", "/")):
            self.event.text = f"/{self.event.text}"


__all__ = ("PrepareCommandMiddleware",)
