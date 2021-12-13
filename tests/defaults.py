# -*- coding: utf-8 -*-
import yaml

from src.configurator import ConfigModel
from src.modules import YamlLoader

EXAMPLE_EVENT = {
    "type": "message_new",
    "object": {
        "message": {
            "date": 1,
            "from_id": 1,
            "id": 1,
            "out": 0,
            "peer_id": 1,
            "text": "some text",
            "conversation_message_id": 1,
            "fwd_messages": [],
            "important": False,
            "random_id": 0,
            "attachments": [],
            "is_hidden": False,
        },
        "client_info": {
            "button_actions": [
                "text",
                "vkpay",
                "open_app",
                "location",
                "open_link",
                "callback",
                "intent_subscribe",
                "intent_unsubscribe",
            ],
            "keyboard": True,
            "inline_keyboard": True,
            "carousel": True,
            "lang_id": 0,
        },
    },
    "group_id": 1,
    "event_id": "event_id",
}


EXAMPLE_CONFIG = """
bot:
    token:
        - FirstToken
        - SecondToken
    admins:
        - 1
        - 2
        - 3
        - 4
    proxy: socks5://some_socks5_proxy:1234
    callback:
        status: true
        host: 0.0.0.0
        port: 6342
        path: /some_path
        secret: some_secret_key

database:
    host: 127.0.0.1
    port: 3306
    user: some_username
    password: some_password
    database: vkbottle_bot_template
    dialect: mysql
    driver: aiomysql
    fix_auto_increment: false
    unix_socket: some_unix_socket
    url: some_url

    redis:
        cache: true
        host: 127.0.0.1
        port: 6379
        user: some_username
        password: some_password
        database: 0
        unix_socket: some_unix_socket
        url: some_url
        time_to_del: 86400
logging:
    log: true
    log_errors: true
    log_console: true
    log_path: logs/%Y-%M-%d_%H-%M-%S.log
    log_errors_path: logs/%Y-%M-%d_%H-%M-%S-error.log
environment:
    status: false
    translate:
        bot:
            token: vk_token
"""


def get_config(config: str) -> ConfigModel:
    """Преобразование yaml в ConfigModel словарь"""
    _config = ConfigModel(**yaml.load(config, YamlLoader))
    return _config
