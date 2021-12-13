# -*- coding: utf-8 -*-
import pytest
from vkbottle_types.events.bot_events import MessageNew

from src.middlewares.NoBotMiddleware import NoBotMiddleware
from src.middlewares.PrepareCommandMiddleware import PrepareCommandMiddleware

from .defaults import EXAMPLE_EVENT


@pytest.mark.asyncio
async def test_no_bot_middleware():
    """Тестирование NoBotMiddleware"""
    BOT_EVENT = MessageNew(**EXAMPLE_EVENT.copy()).object.message
    BOT_EVENT.from_id = -1234

    mw = NoBotMiddleware(event=BOT_EVENT)
    await mw.pre()
    assert mw.error.__str__() == "Groups are not allowed to use bot"

    USER_EVENT = MessageNew(**EXAMPLE_EVENT.copy()).object.message
    mw = NoBotMiddleware(event=USER_EVENT)
    await mw.pre()
    assert not mw.error


@pytest.mark.asyncio
async def test_prepare_command_middleware():
    """Тестирование подготовки команды"""
    FIRST_TEXT_EVENT = MessageNew(**EXAMPLE_EVENT.copy()).object.message
    FIRST_TEXT_EVENT.text = "!cmd"
    FIRST_TEXT_EVENT_EXPECTED = "/cmd"
    SECOND_TEXT_EVENT = MessageNew(**EXAMPLE_EVENT.copy()).object.message
    SECOND_TEXT_EVENT.text = "!!!!!!!!/!/!/!cmd"
    SECOND_TEXT_EVENT_EXPECTED = "/!!!!!!!/!/!/!cmd"
    THIRD_TEXT_EVENT = MessageNew(**EXAMPLE_EVENT.copy()).object.message
    THIRD_TEXT_EVENT.text = "cmd_cmd_cmd/!/!/!"
    THIRD_TEXT_EVENT_EXPECTED = "/cmd_cmd_cmd/!/!/!"
    events = (
        (
            FIRST_TEXT_EVENT,
            FIRST_TEXT_EVENT_EXPECTED,
        ),
        (
            SECOND_TEXT_EVENT,
            SECOND_TEXT_EVENT_EXPECTED,
        ),
        (
            THIRD_TEXT_EVENT,
            THIRD_TEXT_EVENT_EXPECTED,
        ),
    )
    for event, expected_text in events:
        mw = PrepareCommandMiddleware(event=event)
        await mw.pre()
        assert mw.event.text == expected_text
