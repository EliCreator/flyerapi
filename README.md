<div align="left">
    <h1>FlyerAPI<img src="https://telegra.ph/file/e2a2f0526d2937973a70b.png" width=50 height=50></h1>
    <p align="left" >
        <a href="https://pypi.org/project/flyerapi/">
            <img src="https://img.shields.io/pypi/v/flyerapi?style=flat-square" alt="PyPI">
        </a>
        <a href="https://pypi.org/project/flyerapi/">
            <img src="https://img.shields.io/pypi/dm/flyerapi?style=flat-square" alt="PyPI">
        </a>
    </p>
</div>


## Использование

С помощью ``flyerapi`` вы можете использовать <a href="https://api.flyerservice.io/redoc">FlyerAPI</a> вместе с Telegram<br/>
Документация: https://api.flyerservice.io/redoc

## Установка

```bash
pip install flyerapi
```

## Требования
 - ``Python 3.7+``
 - ``aiohttp``

## Возможности
 - ``Asynchronous``
 - ``Exception handling``



## Пример обязательной подписки с использованием aiogram

```python
from flyerapi import Flyer

from aiogram import types


flyer = Flyer(KEY)

async def message_handler(message: types.Message):
    # Применяйте везде, где требуется проверка
    if not await flyer.check(message.from_user.id, language_code=message.from_user.language_code):
        return

async def callback_handler(call: types.CallbackQuery):
    # Применяйте везде, где требуется проверка
    if not await flyer.check(call.from_user.id, language_code=call.from_user.language_code):
        return
```

### Использование пользовательского сообщения

```python
message = {
    'rows': 2,
    'text': '<b>Пользовательский текст</b> для $name',  # HTML

    'button_bot': 'Запустить',
    'button_channel': 'Подписаться',
    'button_url': 'Перейти',
    'button_boost': 'Голосовать',
    'button_fp': 'Выполнить',
}
await flyer.check(user_id, language_code=language_code, message=message)
```


## Пример для заданий

```python
# Получение заданий для пользователя
tasks = await flyer.get_tasks(user_id=user_id, language_code=language_code, limit=5)

# Получиение статуса задания
signature = tasks[0]['signature']  # пример
status = await flyer.check_task(user_id=user_id, signature=signature)

```

### Пример для использования заданий в обязательной подписки с использованием aiogram

Код вынесен в файл: [`examples/check_with_tasks.py`](examples/check_with_tasks.py)


## Пример вебхуков

Код вынесен в файл: [`examples/webhook.py`](examples/webhook.py)


Developed by Eli (c) 2023-2025
