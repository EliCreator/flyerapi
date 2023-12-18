<div align="left">
    <h1>FlyerAPI<img src="https://telegra.ph/file/e2a2f0526d2937973a70b.png" width=30 height=30></h1>
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

With ``flyerapi`` you can use <a href="https://t.me/FlyerServiceBot">FlyerAPI</a> together with Telegram

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

## Basic example

```python
from flyerapi import Flyer

from aiogram import types


flyer = Flyer(key)

async def message_handler(message: types.Message):
    if not await flyer.check(message.from_user.id):
        return

async def callback_handler(call: types.CallbackQuery):
    if not await flyer.check(call.message.from_user.id):
        return
```

Developed by Eli (c) 2023