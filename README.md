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


## Usage

With ``flyerapi`` you can use <a href="https://api.flyerservice.io/redoc">FlyerAPI</a> together with Telegram<br/>
Documentation: https://api.flyerservice.io/redoc

## Installation

```bash
pip install flyerapi
```

## Requirements

 - ``Python 3.7+``
 - ``aiohttp``

## Features

 - ``Asynchronous``
 - ``Exception handling``


## Basic example for a mandatory subscription with aiogram

```python
from flyerapi import Flyer

from aiogram import types


flyer = Flyer(KEY)

async def message_handler(message: types.Message):
    # Use it wherever verification is necessary
    if not await flyer.check(message.from_user.id, language_code=message.from_user.language_code):
        return

async def callback_handler(call: types.CallbackQuery):
    # Use it wherever verification is necessary
    if not await flyer.check(call.from_user.id, language_code=call.from_user.language_code):
        return
```

### Using custom message

```python
message = {
    'text': '<b>Custom text</b> for $name',  # HTML

    'button_bot': 'Start',
    'button_channel': 'Subscribe',
    'button_url': 'Follow',
}
await flyer.check(user_id, language_code=language_code, message=message)
```

## Example for tasks

```python
# Getting tasks for the user
tasks = await flyer.get_tasks(
    user_id=user_id,
    language_code=language_code,  # used only for new pinning
    limit=5,  # used only for new pinning
)

...

# Checking for completed task
status = await flyer.check_task(
    user_id=user_id,
    signature=tasks[0]['signature'],
)


```


Developed by Eli (c) 2023-2024