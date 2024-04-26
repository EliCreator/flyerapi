from cachetools import TTLCache
import time
import logging

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError


logger = logging.getLogger('Flyer')


class Flyer:

    def __init__(self, key: str, debug: bool = False):
        if not isinstance(key, str):
            raise TypeError('key must be a string')

        self.key = key
        self.service_cache_answer = 60
        self.service_shutdown_timeout = 60

        self._cache = TTLCache(maxsize=10000, ttl=self.service_cache_answer)
        self._service_shutdown = 0

        self.debug = debug


    async def _request(self, method: str, params: dict = {}, **kwargs) -> dict:
        url = f'https://api.flyerservice.io/{method}'
        headers = {'Content-Type': 'application/json'}
        data = {'key': self.key, **params}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, **kwargs) as response:
                result = await response.json()

                if self.debug:
                    print(result)

        return result


    async def get_me(self) -> dict:
        """
        Get bot info.

        :return: dict information
        """

        return await self._request('get_me')


    async def check(self, user_id: int, timeout: float=5) -> bool:
        """
        Check user subscription status.

        :param user_id: User ID
        :return: True if subscribed, False otherwise
        """

        if not self.key:
            return True


        if not isinstance(user_id, int):
            logger.error('user_id must be an integer, got {}'.format(type(user_id).__name__))
            return True


        # Chat is not private
        if user_id < 0:
            logger.error('The id is not private')
            return True


        # If the server is not responding
        if self._service_shutdown + self.service_shutdown_timeout >= time.time():
            return True


        # If cached response
        if self._cache.get(user_id, False):
            return True


        try:
            result = await self._request(
                method='check',
                params={'user_id': user_id},
                timeout=timeout,
            )

        # The server is not responding
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


        # Response details
        if 'error' in result:
            logger.error(result['error'])

        elif 'warning' in result:
            logger.warning(result['warning'])

        elif 'info' in result:
            logger.info(result['info'])


        # If response is True, writing in cache
        if result['skip'] and 'error' not in result:
            self._cache[user_id] = True


        return result['skip']