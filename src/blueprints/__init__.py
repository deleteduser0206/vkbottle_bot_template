# -*- coding: utf-8 -*-
"""Содержит разделённый код по файлам с использованием blueprint"""
from src.blueprints import main

bps = (main.bp,)

__all__ = ("bps",)
