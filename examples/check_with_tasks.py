"""
⚠ Внимание:
    Этот файл служит демонстрацией.
    Код может потребовать адаптации под вашу версию aiogram и архитектуру проекта.
"""

import asyncio
from typing import Optional

import aiohttp
from aiogram import types, exceptions, Bot
from flyerapi import Flyer, APIError as FlyerAPIError


bot = Bot(TOKEN)
flyer = Flyer(KEY)


# Настройки сообщения
BUTTONS_ROW = 2
BUTTON_TEXTS = {
    'start bot': '➕ Запустить бота',
    'subscribe channel': '➕ Подписаться',
    'give boost': '➕ Голосовать (3 раза)',  # для лучшей конверсии
    'follow link': '➕ Перейти',
    'perform action': '➕ Выполнить действие',
}
TEXT = """Чтобы получить доступ к функциям бота, <b>необходимо подписаться на ресурсы</b>:"""

_incomplete_statuses = ('incomplete', 'abort')



async def flyer_check_message(user_id: int, language_code: str, message_id: Optional[int] = None) -> bool:
    # Получение заданий для пользователя
    try:
        tasks = await flyer.get_tasks(user_id=user_id, language_code=language_code, limit=5)
    except FlyerAPIError:
        return True
    if not tasks:
        return True

    # Получение только невыполненных заданий
    tasks_incomplete = [
        task for task in tasks
        if task['status'] in _incomplete_statuses
    ]
    if not tasks_incomplete:
        return True

    # создание inline-клавиатуры
    keyboard = {'inline_keyboard': [[]]}
    for task in tasks_incomplete:
        for index, link in enumerate(task['links']):
            button_text = BUTTON_TEXTS.get(task['task'], task['task'])

            # Изменение кнопки для приватных бустов
            if all((
                task['task'] == 'give boost',
                len(task['links']) == 2,
                index == 0,
                'subscribe channel' in BUTTON_TEXTS,
            )):
                button_text = BUTTON_TEXTS['subscribe channel']

            if len(keyboard['inline_keyboard'][-1]) == BUTTONS_ROW:
                keyboard['inline_keyboard'].append([])

            keyboard['inline_keyboard'][-1].append({
                'text': button_text,
                'url': link,
            })

    keyboard['inline_keyboard'].append([{
        'text': '☑️ Проверить',
        'callback_data': 'flyer_check',
    }])

    if message_id is None:
        await bot.send_message(
            chat_id=user_id,
            text=TEXT,
            parse_mode='HTML',
            reply_markup=keyboard,
        )
    else:
        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=TEXT,
                parse_mode='HTML',
                reply_markup=keyboard,
            )
        except exceptions.MessageNotModified:
            pass
    return False


async def flyer_check(user_id: int) -> bool:
    # Получение заданий для пользователя
    try:
        tasks = await flyer.get_tasks(user_id=user_id)
    except FlyerAPIError:
        return True
    if not tasks:
        return True

    # Получение только невыполненных заданий
    tasks_incomplete = [
        task for task in tasks
        if task['status'] in _incomplete_statuses
    ]
    if not tasks_incomplete:
        return True

    asyncio_tasks = [
        flyer.check_task(user_id=user_id, signature=task['signature'])
        for task in tasks_incomplete
    ]
    results = await asyncio.gather(*asyncio_tasks, return_exceptions=True)

    for index, (task, status) in enumerate(zip(tasks_incomplete, results)):
        if isinstance(status, str):
            tasks[index]['status'] = status

    return all([task['status'] not in _incomplete_statuses for task in tasks])



# Обработчик: Проверка подписки
async def call_flyer_check(call: types.CallbackQuery):
    # Проверка подписок
    if not await flyer_check(call.from_user.id):
        if not await flyer_check_message(
            user_id=call.from_user.id,
            language_code=call.from_user.language_code,
            message_id=call.message.message_id,
        ):
            await call.answer()
            return

    await call.message.delete()

    ...


# Обработчик: Сообщение (пример)
async def message_handler(message: types.Message):
    # Применяйте везде, где требуется проверка
    if not await flyer_check_message(
        user_id=message.from_user.id,
        language_code=message.from_user.language_code,
    ):
        return

    ...