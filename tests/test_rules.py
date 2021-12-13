# -*- coding: utf-8 -*-
import pytest
from vkbottle_types.events.bot_events import MessageNew

from src.rules import IsAdminRule

from .defaults import EXAMPLE_CONFIG, EXAMPLE_EVENT, get_config


@pytest.mark.asyncio
async def test_admin_rule():
    """Тестирование AdminRule"""
    config = get_config(config=EXAMPLE_CONFIG)
    NORMAL_EVENT = MessageNew(**EXAMPLE_EVENT.copy()).object.message
    WRONG_EVENT = MessageNew(**EXAMPLE_EVENT.copy()).object.message
    WRONG_EVENT.from_id = -4321
    rule = IsAdminRule(config=config)

    assert await rule.check(NORMAL_EVENT) is True
    assert await rule.check(WRONG_EVENT) is False
