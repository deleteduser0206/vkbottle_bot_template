# -*- coding: utf-8 -*-
"""Содержит разделённый код по файлам с использованием blueprint"""
from src.blueprints import admin, main

bps = (
    main.bp,
    admin.bp,
)

__all__ = ("bps",)
