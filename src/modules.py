# -*- coding: utf-8 -*-
"""Импорты библиотек с возможными проблемами на разных версиях питона, для лёгкой замены"""
import orjson as json
from loguru import logger
from yaml import CLoader as YamlLoader

__all__ = (
    "json",
    "YamlLoader",
    "logger",
)
