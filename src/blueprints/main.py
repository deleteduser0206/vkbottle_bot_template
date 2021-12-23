# -*- coding: utf-8 -*-
"""Модуль с основными командами"""
from datetime import datetime
from typing import Optional

from vkbottle.bot import Blueprint, Message, rules

from src.configurator import config
from src.database.repositories.user import UserRepository
from src.rules import IsAdminRule

bp = Blueprint(name="main blueprint")
bp.labeler.vbml_ignore_case = True


@bp.on.message(payload={"cmd": "start"})
@bp.on.message(text=["/начать", "/start"])
async def start_handler(_):
    """Обработчик, который приветствует при команде /start|/начать или payload: {"cmd": "start"}"""
    return "Привет!\n" "Это пример бота.\nУзнать мои команды: /help"


@bp.on.message(text=["/register", "/register <!>"])
async def register_handler(m: Message):
    """Обработчик для создания пользователя"""
    user = UserRepository(uid=m.from_id)
    if await user.register(ctx_api=m.ctx_api):
        return "Вы успешно зарегистрировались."

    return f"Вы уже зарегистрированы, ваш профиль:\n\n{await user.get_prepared_user_info()}"


@bp.on.message(
    text=[
        "/unregister<!>",
        "/delete<!>",
        "/delete_account<!>",
    ]
)
async def delete_account_handler(m: Message):
    """Обработчик для удаления пользователя по его команде"""
    if await UserRepository(uid=m.from_id).unregister():
        return "Вы успешно удалили аккаунт."

    return "Вы не зарегистрированы. \nВведите /register"


@bp.on.message(text=["/profile", "/profile <id_:int>", "/profile [id<id_:int>|<!>]"])
async def profile_handler(m: Message, id_: Optional[int] = None):
    """Обработчик получения информации о пользователе"""
    if await IsAdminRule().check(event=m) and isinstance(id_, int):
        user = await UserRepository(uid=id_).get_full_user_info()
        if not user:
            return "Пользователя нет в базе данных."

        info = UserRepository.prepared_info(user=user)
        return f"Профиль пользователя [id{m.from_id}|{user.first_name}]:\n{info}"

    user = await UserRepository(uid=m.from_id).get_prepared_user_info()
    return user


@bp.on.message(text=["/time<!>"])
async def current_time_handler(m: Message):
    """
    Обработчик с отправкой текущего времени пользователю,
    с использованием времени от события,
    которое приходит вместе с сообщением
    """
    datetime_template = "Текущее время: %H:%M:%S\nДата: %d.%m.%Y"
    return datetime.fromtimestamp(m.date).strftime(datetime_template)


@bp.on.message(text=["/command<!>", "/help<!>"])
async def help_list_handler(_):
    """Выводит список команд пользователю"""
    text = (
        "Мой список команд:\n"
        "/register - Зарегистрировать аккаунт\n"
        "/unregister - Удалить аккаунт\n"
        "/time - Текущее время\n"
        "/help - Список команд\n"
    )
    return text


@bp.on.message(rules.ChatActionRule(["chat_invite_user"]))
async def chat_invite_handler(m: Message):
    """Обработчик с информацией о том, что нашего бота пригласили"""
    if m.action.member_id == -config.bot.info.group_id:
        return "Спасибо что пригласили меня!\nВведите /help для получения списка команд."
