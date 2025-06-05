from typing import Optional, Union, Dict, List
from cachetools import TTLCache
import time
import logging

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError


logger = logging.getLogger('Flyer')


class APIError(Exception):
    pass


class Flyer:
    """
        https://api.flyerservice.io/redoc
    """

    def __init__(self, key: str, debug: bool = False, **request_kwargs):
        if not isinstance(key, str):
            raise TypeError('key must be a string')

        self.key = key
        self.debug = debug
        self.service_shutdown_timeout = 60
        self.request_kwargs = request_kwargs

        service_cache_answer = 60
        self._cache = TTLCache(maxsize=10000, ttl=service_cache_answer)
        self._service_shutdown = 0


    async def _request(self, method: str, params: dict = {}) -> dict:
        url = f'https://api.flyerservice.io/{method}'
        headers = {'Content-Type': 'application/json'}
        data = {'key': self.key, **params}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, **self.request_kwargs) as response:
                result = await response.json()

                if self.debug:
                    print(result)

        # Response details
        if 'error' in result:
            logger.error(result['error'])

        elif 'warning' in result:
            logger.warning(result['warning'])

        elif 'info' in result:
            logger.info(result['info'])

        return result


    async def get_me(self) -> dict:
        """
        Get bot info.

        :return: dict information
        """
        return await self._request('get_me')


    async def check(self,
        user_id: int,
        language_code: Optional[str] = None,
        message: Dict[str, str] = {},
    ) -> bool:
        """
        Check user subscription status.

        :param user_id: User ID
        :param language_code: Language code of user ID
        :param message: Custom message

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


        params = {'user_id': user_id}
        if isinstance(language_code, str):
            params['language_code'] = language_code
        if message:
            params['message'] = message

        try:
            result = await self._request(
                method='check',
                params=params,
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


        # If response is True, writing in cache
        if result['skip'] and 'error' not in result:
            self._cache[user_id] = True

        # Calling an exception
        if 'skip' not in result and 'error' in result:
            raise APIError(result['error'])

        return result['skip']


    async def get_tasks(self,
        user_id: int,
        language_code: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        """
        Getting tasks from the service.

        :param user_id: User ID
        :param language_code: Language code of user ID
        :param limit: The maximum number of resources to search for

        :return: List of resources
        """

        if not self.key:
            return []


        if not isinstance(user_id, int):
            logger.error('user_id must be an integer, got {}'.format(type(user_id).__name__))
            return []


        # Chat is not private
        if user_id < 0:
            logger.error('The id is not private')
            return []


        # If the server is not responding
        if self._service_shutdown + self.service_shutdown_timeout >= time.time():
            return []


        params = {'user_id': user_id}
        if isinstance(language_code, str):
            params['language_code'] = language_code
        if isinstance(limit, int):
            params['limit'] = limit

        try:
            result = await self._request(
                method='get_tasks',
                params=params,
            )

        # The server is not responding
        except (ClientConnectorError, TimeoutError):
            self._service_shutdown = time.time()
            return []

        # Answer error
        except ContentTypeError as e:
            logger.error(f'Request: {str(e)}')
            return []

        # Another error
        except Exception as e:
            logger.error(f'Request: {str(e)}')
            return []


        # Calling an exception
        if 'result' not in result and 'error' in result:
            raise APIError(result['error'])

        return result['result']


    async def check_task(self, user_id: int, signature: str) -> Union[str, None]:
        """
        Getting the result of completing the task.

        :param user_id: User ID
        :param signature: The signature of the resource for identification

        :return: Resource status
        """

        if not self.key:
            return None


        if not isinstance(user_id, int):
            logger.error('user_id must be an integer, got {}'.format(type(user_id).__name__))
            return None


        # Chat is not private
        if user_id < 0:
            logger.error('The id is not private')
            return None


        # If the server is not responding
        if self._service_shutdown + self.service_shutdown_timeout >= time.time():
            return None


        params = {'user_id': user_id, 'signature': signature}

        try:
            result = await self._request(
                method='check_task',
                params=params,
            )

        # The server is not responding
        except (ClientConnectorError, TimeoutError):
            self._service_shutdown = time.time()
            return None

        # Answer error
        except ContentTypeError as e:
            logger.error(f'Request: {str(e)}')
            return None

        # Another error
        except Exception as e:
            logger.error(f'Request: {str(e)}')
            return None


        # Calling an exception
        if 'result' not in result and 'error' in result:
            raise APIError(result['error'])

        return result['result']


    async def get_tasks(self,
        user_id: int,
        language_code: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        """
        Getting tasks from the service.

        :param user_id: User ID
        :param language_code: Language code of user ID
        :param limit: The maximum number of resources to search for

        :return: List of resources
        """

        if not self.key:
            return []


        if not isinstance(user_id, int):
            logger.error('user_id must be an integer, got {}'.format(type(user_id).__name__))
            return []


        # Chat is not private
        if user_id < 0:
            logger.error('The id is not private')
            return []


        # If the server is not responding
        if self._service_shutdown + self.service_shutdown_timeout >= time.time():
            return []


        params = {'user_id': user_id}
        if isinstance(language_code, str):
            params['language_code'] = language_code
        if isinstance(limit, int):
            params['limit'] = limit

        try:
            result = await self._request(
                method='get_tasks',
                params=params,
            )

        # The server is not responding
        except (ClientConnectorError, TimeoutError):
            self._service_shutdown = time.time()
            return []

        # Answer error
        except ContentTypeError as e:
            logger.error(f'Request: {str(e)}')
            return []

        # Another error
        except Exception as e:
            logger.error(f'Request: {str(e)}')
            return []


        # Calling an exception
        if 'result' not in result and 'error' in result:
            raise APIError(result['error'])

        return result['result']


    async def get_completed_tasks(self, user_id: int) -> Union[dict, None]:

        if not self.key:
            return None


        if not isinstance(user_id, int):
            logger.error('user_id must be an integer, got {}'.format(type(user_id).__name__))
            return None


        # Chat is not private
        if user_id < 0:
            logger.error('The id is not private')
            return None


        # If the server is not responding
        if self._service_shutdown + self.service_shutdown_timeout >= time.time():
            return None


        params = {'user_id': user_id}

        try:
            result = await self._request(
                method='get_completed_tasks',
                params=params,
            )

        # The server is not responding
        except (ClientConnectorError, TimeoutError):
            self._service_shutdown = time.time()
            return None

        # Answer error
        except ContentTypeError as e:
            logger.error(f'Request: {str(e)}')
            return None

        # Another error
        except Exception as e:
            logger.error(f'Request: {str(e)}')
            return None


        # Calling an exception
        if 'result' not in result and 'error' in result:
            raise APIError(result['error'])

        return result['result']