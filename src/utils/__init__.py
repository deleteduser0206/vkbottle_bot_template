# -*- coding: utf-8 -*-
"""
Модуль с утилитами, которые по каким-то причинам не могут быть в другом месте.
"""
from uvloop import EventLoopPolicy
from vkbottle.tools.dev.loop_wrapper import LoopWrapper

loop = EventLoopPolicy().get_event_loop()
loop_wrapper = LoopWrapper()


__all__ = (
    "loop",
    "loop_wrapper",
)
