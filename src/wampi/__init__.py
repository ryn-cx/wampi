# TODO: Validate
"""Contains the Wampi class."""

from __future__ import annotations

import time
from http import HTTPStatus
from json import JSONDecodeError, loads
from logging import NullHandler, getLogger
from typing import TYPE_CHECKING, Any

from get_around import GetAround

from wampi.constants import BASE_API_URL
from wampi.exceptions import HTTPError, ResourceNotFoundError, UnauthorizedError
from wampi.title_sources import TitleSources

if TYPE_CHECKING:
    import httpx

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Wampi:
    """Watchmode API wrapper.

    Only the title sources endpoint is wrapped, every other Watchmode endpoint
    is out of scope: https://api.watchmode.com/docs
    """

    def __init__(
        self,
        api_key: str,
        get_around_client: GetAround | None = None,
    ) -> None:
        """Initialize the Wampi client.

        Args:
            api_key: Watchmode API key. Reading it from a credential store is
                the caller's job.
            get_around_client: HTTP client to use. Defaults to a direct client.
        """
        self.api_key = api_key
        self.get_around_client = get_around_client or GetAround()

        self.title_sources = TitleSources(self)

    def download(
        self,
        endpoint: str,
        params: dict[str, Any],
        log_id: str,
    ) -> list[dict[str, Any]]:
        """Downloads from the API.

        Parameters whose value is `None` are dropped so an optional filter is
        only sent when it was explicitly given.

        Every wrapped endpoint answers with a JSON array, so a response that
        holds anything else is treated as an error even when it came back with
        a successful status code.
        """
        url = f"{BASE_API_URL}/{endpoint}"
        # The key can also be sent as an `apiKey` query parameter, but that is
        # the legacy method and it leaks the key into logged URLs.
        headers = {"accept": "application/json", "X-API-Key": self.api_key}

        logger.debug("Downloading: %s", log_id)
        start = time.monotonic()
        response = self.get_around_client.get(
            url,
            params={key: value for key, value in params.items() if value is not None},
            headers=headers,
        )
        self._raise_for_status(response)

        parsed = _parsed_or_raw(response.text)
        if not isinstance(parsed, list):
            raise HTTPError(response.status_code, parsed)

        logger.debug("Downloaded %s (%.4f s)", log_id, time.monotonic() - start)
        return parsed

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        """Raises the error that matches the status code of `response`."""
        if response.status_code == HTTPStatus.OK:
            return

        body = _parsed_or_raw(response.text)
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError(response.status_code, body)
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise ResourceNotFoundError(response.status_code, body)
        raise HTTPError(response.status_code, body)


def _parsed_or_raw(body: str) -> Any:  # noqa: ANN401 - A response body can be any JSON value.
    """Return `body` parsed as JSON, or the raw text if it is not JSON."""
    try:
        return loads(body)
    except JSONDecodeError:
        return body
