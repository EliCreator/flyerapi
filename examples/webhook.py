import uvicorn
from fastapi import FastAPI, Request


ANSWER = {'status': True}

app = FastAPI()


@app.post('/flyer_webhook')
async def webhook_handler(request: Request):
    data = await request.json()
    print(request.client)

    # для проверки работы вебхука
    if data['type'] == 'test':
        return ANSWER


    # обязательная подписка пройдена
    elif data['type'] == 'sub_completed':
        
        pass  # сообщение для пользователя

        return ANSWER


    # новый статус задания: отписка от канала
    elif data['type'] == 'new_status' and data['data']['status'] == 'abort':

        pass  # попытка вернуть пользователя в канал

        return ANSWER


    return ANSWER


if __name__ == '__main__':
    # api.flyerservice.io/redoc/webhook
    uvicorn.run(app, host='0.0.0.0', port=50000)