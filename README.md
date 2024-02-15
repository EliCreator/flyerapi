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

## Basic example with aiogram

```python
from flyerapi import Flyer

from aiogram import types


flyer = Flyer(KEY)

async def message_handler(message: types.Message):
    if not await flyer.check(message.from_user.id):
        return

async def callback_handler(call: types.CallbackQuery):
    if not await flyer.check(call.from_user.id):
        return
```
## C# Installation
 Execute this method on Flyer check
- Returns **True** if user has done all tasks for Flyer, otherwise **False**
- Instead of **TOKEN_FLYER** use **API key from Flyer**
```csharp
        private async Task<bool> IsUserRegisteredFlyerCheck(long userId)
        {
            const int TIMEOUT_SECONDS = 2;
            try
            {
                using var client = new HttpClient();
                client.Timeout = TimeSpan.FromSeconds(TIMEOUT_SECONDS);

                var sendPostDto = new { key = TOKEN_FLYER, user_id = userId };
                var json = JsonConvert.SerializeObject(sendPostDto);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await client.PostAsync("https://api.flyerservice.io/check", content);

                var result = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                {
                    Log.Error("==> ERROR ON FLYER RESPONSE:" + result);
                    return true;
                }

                if (result.Contains("\"skip\":false"))
                {
                    Log.Information($"Flyer ==> tasks not done, userId: {userId}");
                    return false;
                }
                else if (result.Contains("\"skip\":true"))
                {
                    Log.Information($"Flyer ==> tasks done, userId: {userId}, result: {result}");
                    return true;
                }

                Log.Fatal($"Flyer ==> wrong result: {result}");
                return true; //true on error
            }
            catch (TaskCanceledException)
            {
                Log.Error($"TIMEOUT FLYER - {TIMEOUT_SECONDS}s");
                return true; //true on error
            }
            catch (Exception ex)
            {
                Log.Error(ex, "Error FLYER HTTP: ");
                return true; //true on error
            }
        }
```

Developed by Eli (c) 2024
