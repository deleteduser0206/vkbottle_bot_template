# -*- coding: utf-8 -*-
"""Модуль с моделью пользователя"""
import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.database.models.db import Base


class User(Base):
    """Модель пользователя"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(32))
    last_name = Column(String(32))
    created_at = Column(DateTime, default=datetime.datetime.now)
