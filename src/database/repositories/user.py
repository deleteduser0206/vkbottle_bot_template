# -*- coding: utf-8 -*-
"""Шаблоны выполнения запросов в базе данных"""
from typing import Optional, Union

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from vkbottle import ABCAPI, API

from src.configurator import config
from src.database.models.db import engine, session
from src.database.models.user import User
from src.modules import json, logger
from src.redis import redis


class UserRepository:
    def __init__(self, uid: int):
        self.uid = uid

    async def register(self, ctx_api: Union[API, ABCAPI]) -> bool:
        """Регистрация пользователя в базе данных"""

        if await self.get_full_user_info():
            return False

        try:
            if config.database.fix_auto_increment:
                async with session as conn:
                    await conn.execute("ALTER TABLE `users` auto_increment = 1;")
                    await conn.commit()

            async with engine.connect() as conn:
                vk_user = (await ctx_api.users.get(user_id=self.uid))[0]
                query = insert(User).values(
                    uid=self.uid, first_name=vk_user.first_name, last_name=vk_user.last_name
                )
                await conn.execute(query)

            logger.success(f"Пользователь {self.uid} успешно зарегистрирован")
            return True

        except IntegrityError:
            return False

        except Exception:  # noqa
            return False

    async def unregister(self):
        """Удаление записи о пользователе из redis и базы данных"""
        if redis:
            async with redis.client() as conn:
                await conn.delete(f"full_user_info_{self.uid}")

        try:
            async with engine.connect() as conn:
                query = delete(User).where(User.uid == self.uid)
                await conn.execute(query)
        except IntegrityError:
            return False
        else:
            return True

    async def get_full_user_info(self):
        """
        Получение полной информации о пользователе в необработанном виде
        и занесение в redis при необходимости
        """
        if redis:
            async with redis.client() as conn:
                cache_info = await conn.get(f"full_user_info_{self.uid}")

            if cache_info:
                cache_info = User(**json.loads(cache_info))
                return cache_info

            async with engine.connect() as conn:
                query = select(User).where(User.uid == self.uid)
                user: Optional[User] = (await conn.execute(query)).fetchone()

            if not user:
                return None

            async with redis.client() as conn:
                await conn.setex(
                    f"full_user_info_{self.uid}",
                    config.database.redis.time_to_del,
                    value=json.dumps(dict(user)),
                )

            return user

        async with engine.connect() as conn:
            query = select(User).where(User.uid == self.uid)
            user: Optional[User] = (await conn.execute(query)).fetchone()

        return user

    async def get_prepared_user_info(self) -> str:
        """Получение информации о пользователе в красивом виде"""
        user = await self.get_full_user_info()
        return self.prepared_info(user=user)

    @staticmethod
    def prepared_info(user: Optional[User]) -> str:
        """Получает сырую информацию о пользователе и возвращает в красивом виде"""
        if user:
            return (
                f"ID: {user.uid}\n"
                f"ID в БД: {user.id}\n"
                f"Имя: {user.first_name}\n"
                f"Фамилия: {user.last_name}\n"
                f"Дата регистрации в боте: {user.created_at}\n"
            )

        return "Пользователя нет в базе данных."


__all__ = ("UserRepository",)
