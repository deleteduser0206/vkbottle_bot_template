# VKBottle Bot Template


## Описание

Шаблон бота на фреймворк VKBottle 4-й версии:

- Кэш, основанный на Redis.
- База данных для пользователей.
- Запуск через Docker.
- Возможность установить прокси для подключения к API.

---

## Навигация

В пакете [**src**](src) находится основной код проекта, в коде более подробное описание. Его содержимое:

- [blueprints](src/blueprints) - разделение
  кода. [(?)](https://vkbottle.readthedocs.io/ru/latest/tutorial/code-separation/)
- [middlewares](src/middlewares) - прослойка для выполнения действий до/после обработки
  события. [(?)](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/middleware/)
- [rules](src/rules) - правила. [(?)](https://vkbottle.readthedocs.io/ru/latest/tutorial/rules/)
- [database](src/database)
    - [models](src/database/models) - модели, инициализация базы данных.
    - [repositories](src/database/repositories) - репозитории.
- [utils](src/utils) - утилиты, которые почему-то не должны находиться в том файле, где они используются.
- [web](src/web) - веб-часть проекта, в виде сервера используется aiohttp.web.
- [custom](src/custom) - часть проекта для модифицированных модулей.
- [\_\_main\_\_.py](src/__main__.py) - точка входа. Необходим для запуска приложений.
- [app.py](src/app.py) - инициализация/настройка приложений, содержит экземпляр бота & веб приложения.
- [bot.py](src/bot.py) - модифицированный класс создания бота.
- [configurator.py](src/configurator.py) - модуль с конфигурацией проекта, которая берётся из файла config.yml,
  переменных окружения(опционально).
- [initialize.py](src/initialize.py) - запуск синхронных/асинхронных функций при старте проекта.
- [modules.py](src/modules.py) - легко-заменяемые модули, с которыми могут быть проблемы на разных платформах/версиях.
  Так же здесь присутствует модуль логирования.
- [redis.py](src/redis.py) - инициализация redis.

В [tests](tests) находятся тесты:
- [test_config_model.py](tests/test_config_model.py) - тестирование модели конфига.
- [test_rules.py](tests/test_rules.py) - тестирование правил
- [test_middleware.py](tests/test_middleware.py) - тестирование middlewares

---

## Как это запустить?

### Зависимости

- Python версии 3.7.2 и выше.
- SQL Server.
- Redis (необязательно).
- Docker (необязательно).

### Подготовка:

1. Создание & Активация виртуального окружения

```shell
# Установка venv
python -m pip install venv

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
source venv/bin/activate
```
```shell
# Установка poetry, если вы этого не сделали
python -m pip install poetry

# Создаём виртуальное окружение
make venv
```

2. Установка poetry

```shell
python -m pip install poetry
```

3. Установка зависимостей

```shell
# Для установки дев зависимостей
poetry install
# Или
poetry install --no-dev
# Для установки продакшн зависимостей
```
```shell
# Для установки продакшн зависимостей
make install
# Или
make install-dev
# Для установки дев зависимостей
```

4. Переименовать/скопировать **config.yml.example** в **config.yml** и настроить его.

```shell
# Копируем config.example.yml
cp config.example.yml config.yml
# Редактируем файл редактором nano
nano config.yml
```

---

### Запуск бота

1. Запуск бота вместе с базой данных через docker-compose. (**Рекомендуется**)

```shell
# Сборка и запуск контейнеров
docker-compose up --build
# Сборка и запуск контейнеров в фоновом режиме
docker-compose up --build -d
# Остановить контейнеры поле запуска в фоновом режиме
docker-compose down
```

2. Сборка и запуск контейнера через Docker

```shell
docker build -t vkbottle_bot_template .
docker run vkbottle_bot_template
# Или
docker run -d vkbottle_bot_template
# Для запуска в фоновом режиме
```

3. Ручной запуск
```shell
python3 -m src
# Или
python3 src/__main__.py
```

---

## TODO

- [StateDispenser](src/custom/StateDispenser.py) с Redis
- Автоматический выбор секретного ключа в [callback](src/web/callback.py)
- Рефакторинг [репозитория пользователя](src/database/repositories/user.py)

---

## Лицензия
Данный проект не имеет лицензии, можете использовать все файлы из данного проекта как вам угодно.

Некоторые вещи взял из:
- [vkbottle](https://github.com/vkbottle/vkbottle) 
  - [Makefile](Makefile)

- [vkbottle_bot_architecture_example](https://github.com/nomilkinmyhome/vkbottle_bot_architecture_example)