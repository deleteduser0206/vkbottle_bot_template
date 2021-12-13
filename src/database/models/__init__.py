# -*- coding: utf-8 -*-
"""Модуль с моделями"""
from src.database.models import db
from src.database.models.user import User

__all__ = (
    "User",
    "db",
)
