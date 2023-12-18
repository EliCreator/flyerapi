import time

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError


class Flyer:

    def __init__(self, key: str):
        self.key = key
        self.service_shutdown_timeout = 60 * 5
        self._service_shutdown = 0

    async def check(self, user_id: int, timeout: float=5, see_print: bool=True) -> bool:
        """
        Check user subscription status.

        :param user_id: User ID
        :return: True if subscribed, False otherwise
        """

        # If the server is not responding
        if self._service_shutdown * self.service_shutdown_timeout >= time.time():
            return True

        try:
            url = 'https://api.flyerservice.io/check'
            headers = {'Content-Type': 'application/json'}
            data = {'key': self.key, 'user_id': user_id}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data, timeout=timeout) as response:
                    result = await response.json()

        # If the server is not responding
        except (ClientConnectorError, TimeoutError):
            self._service_shutdown = time.time()
            return True

        # Another error
        except Exception as e:
            if see_print:
                print(f'Flyer request error: {str(e)}')
            return True

        # Warning notification
        if see_print:
            if 'error' in result:
                print('Flyer error: {}'.format(result['error']))
            elif 'warning' in result:
                print('Flyer warning: {}'.format(result['warning']))
            elif 'info' in result:
                pass

        return result['skip']