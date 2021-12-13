# -*- coding: utf-8 -*-
"""Модуль с middlewares"""
from src.middlewares import NoBotMiddleware, PrepareCommandMiddleware, UnknownCommandMiddleware

mws = (
    NoBotMiddleware.NoBotMiddleware,
    UnknownCommandMiddleware.UnknownCommandMiddleware,
    PrepareCommandMiddleware.PrepareCommandMiddleware,
)

__all__ = ("mws",)
