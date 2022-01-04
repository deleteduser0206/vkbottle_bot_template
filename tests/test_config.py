# -*- coding: utf-8 -*-

from src.configurator import ConfigModel, get_config

from .defaults import EXAMPLE_CONFIG, EXAMPLE_CONFIG_WITH_ENVIRONMENT_VALUES


def test_config_model_without_environment_values():
    """Тестирование преобразования"""
    config: ConfigModel = get_config(string=EXAMPLE_CONFIG)
    assert isinstance(config, ConfigModel)
    assert config.bot.token == ["FirstToken", "SecondToken"]
    assert config.bot.admins == [1, 2, 3, 4]
    assert config.bot.proxy == "socks5://some_socks5_proxy:1234"

    assert config.bot.callback.status is True
    assert config.bot.callback.host == "0.0.0.0"
    assert config.bot.callback.port == 6342
    assert config.bot.callback.path == "/some_path"
    assert config.bot.callback.secret == "some_secret_key"

    assert config.database.host == "127.0.0.1"
    assert config.database.port == 3306
    assert config.database.user == "some_username"
    assert config.database.password == "some_password"
    assert config.database.database == "vkbottle_bot_template"
    assert config.database.dialect == "mysql"
    assert config.database.driver == "aiomysql"
    assert config.database.fix_auto_increment is False
    assert config.database.unix_socket == "some_unix_socket"
    assert config.database.url == "some_url"

    assert config.database.redis.cache is True
    assert config.database.redis.host == "127.0.0.1"
    assert config.database.redis.port == 6379
    assert config.database.redis.user == "some_username"
    assert config.database.redis.password == "some_password"
    assert config.database.redis.database == 0
    assert config.database.redis.unix_socket == "some_unix_socket"
    assert config.database.redis.url == "some_url"
    assert config.database.redis.time_to_del == 86400

    assert config.logging.log is True
    assert config.logging.log_errors is True
    assert config.logging.log_console is True
    assert config.logging.log_path == "logs/%Y-%M-%d_%H-%M-%S.log"
    assert config.logging.log_errors_path == "logs/%Y-%M-%d_%H-%M-%S-error.log"


def test_config_model_with_environment_values():
    """Тестирование преобразования"""
    try:
        get_config(string=EXAMPLE_CONFIG_WITH_ENVIRONMENT_VALUES)
    except ValueError:
        assert True
    else:
        assert False
