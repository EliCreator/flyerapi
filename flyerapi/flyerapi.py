import time
import logging

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError


logger = logging.getLogger('Flyer')


class Flyer:

    def __init__(self, key: str):
        if not isinstance(key, str):
            raise TypeError('key must be a string')

        self.key = key
        self.service_shutdown_timeout = 60
        self._service_shutdown = 0


    async def check(self, user_id: int, timeout: float=5) -> bool:
        """
        Check user subscription status.

        :param user_id: User ID
        :return: True if subscribed, False otherwise
        """

        if not isinstance(user_id, int):
            logger.error('user_id must be an integer, got {}'.format(type(user_id).__name__))
            return True


        # If the server is not responding
        if self._service_shutdown + self.service_shutdown_timeout >= time.time():
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

        # Answer error
        except ContentTypeError as e:
            logger.error(f'Request: {str(e)}')
            return True

        # Another error
        except Exception as e:
            logger.error(f'Request: {str(e)}')
            return True


        # Warning notification
        if 'error' in result:
            logger.error(result['error'])

        elif 'warning' in result:
            logger.warning(result['warning'])

        elif 'info' in result:
            logger.info(result['info'])


        return result['skip']
