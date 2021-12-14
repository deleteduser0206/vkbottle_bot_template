# -*- coding: utf-8 -*-
from vkbottle.bot import Blueprint

from src.modules import logger
from src.rules import IsAdminRule

bp = Blueprint(name="admin commands")
bp.labeler.vbml_ignore_case = True
bp.labeler.auto_rules.append(IsAdminRule())


@bp.on.message(text="/stop_polling")
async def stop_polling_handler(_):
    from src.app import bot

    bot._polling.stop = True  # noqa
    logger.info("Polling stopped")
    return "Polling stopped"
