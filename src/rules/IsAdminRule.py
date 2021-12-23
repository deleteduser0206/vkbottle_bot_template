# -*- coding: utf-8 -*-
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from src.configurator import ConfigModel as ConfigModel
from src.configurator import config as config_


class IsAdminRule(ABCRule[Message]):
    def __init__(self, config: ConfigModel = config_):
        self.config: ConfigModel = config

    async def check(self, event: Message) -> bool:
        """
        Функция проверяет что пользователь,
        который отправил команду предназначенную для администраторов, является ним
        """
        if event.from_id in self.config.bot.admins:
            return True

        return False
