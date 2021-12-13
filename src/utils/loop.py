# -*- coding: utf-8 -*-
"""Модуль с loop от uvloop и loop_wrapper"""
from uvloop import EventLoopPolicy
from vkbottle.tools.dev.loop_wrapper import LoopWrapper

loop = EventLoopPolicy().get_event_loop()
loop_wrapper = LoopWrapper()
