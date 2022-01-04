# -*- coding: utf-8 -*-
"""Импорты библиотек с возможными проблемами на разных версиях питона, для лёгкой замены"""
from vkbottle.modules import json, logger
from yaml import CLoader as YamlLoader

__all__ = (
    "json",
    "YamlLoader",
    "logger",
)
