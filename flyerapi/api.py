import time
import logging

from typing import Any, Dict, Union

from aiohttp import ClientConnectorError, ClientSession, ClientTimeout
from pydantic import ValidationError

from .models import CheckResponse


log = logging.getLogger("flyer")

class Flyer(object):

    BASE_URL = "https://api.flyerservice.io"
    SERVICE_SHUTDOWN_TIMEOUT = 60

    def __init__(self, key: str) -> None:
        """
        Create flyerapi instance

        :param str key: API key
        """

        self.key = key
        self.session = ClientSession(base_url=self.BASE_URL)
        self._service_shutdown = 0.0

    async def _request(self, endpoint: str, data: Dict[str, Any], timeout: Union[int, float]=5) -> Any:
        """
        Base request method

        :param str endpoint: API endpoint
        :param Dict[str, Any] data: JSON data
        :param Union[int, float] timeout: API request timeout, defaults to 5
        :return Any: API response
        """

        data.update(key=self.key)
        async with self.session.post(
            endpoint,
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=ClientTimeout(total=timeout),
        ) as response:
            return response.json(content_type=None)

    async def check(self, user_id: int, timeout: Union[int, float]=5) -> bool:
        """
        Check user subscription status.

        :param user_id: User ID
        :return: True if subscribed, False otherwise
        """

        if self._service_shutdown + self.SERVICE_SHUTDOWN_TIMEOUT >= time.time():
            return True

        try:
            response = await self._request(
                "/check",
                data={"user_id": user_id},
                timeout=timeout,
            )
            data = CheckResponse(**response)
        except (ClientConnectorError, TimeoutError):
            self._service_shutdown = time.time()
            return True
        except ValidationError:
            log.error("Invalid response: %s", response)

        if data.info:
            log.info(data.info)
        elif data.warning:
            log.warning(data.warning)
        elif data.error:
            log.error(data.error)

        return response.skip

    async def close(self) -> None:
        """
        Closes FlyerAPI's session
        """
        if not self.session.closed:
            await self.session.close()
