from __future__ import annotations

from http import HTTPStatus
from logging import NullHandler, getLogger
from time import monotonic
from typing import Any

from get_around import GetAround

from wampi.exceptions import (
    HTTPError,
    ResourceNotFoundError,
    UnauthorizedError,
)
from wampi.title_sources import GetTitleSources


logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Wampi:
    """Watchmode title sources API wrapper."""

    def __init__(
        self,
        api_key: str,
        get_around_client: GetAround | None = None,
    ) -> None:
        """Initialize the Wampi client.

        Args:
            api_key: Watchmode API key.
            get_around_client: Get Around client to route requests through.
        """
        self.api_key = api_key
        self.get_around_client = get_around_client or GetAround()

        self.title_sources = GetTitleSources(self).fetch

    def download(
        self,
        endpoint: str,
        params: dict[str, Any],
        log_id: str,
    ) -> list[dict[str, Any]]:
        """Download the response from Watchmode.

        Args:
            endpoint: The API endpoint to download data from.
            params: The query parameters to send with the request.
            log_id: A unique identifier for the request.

        Raises:
            ResourceNotFoundError: If the params are invalid.
            UnauthorizedError: If the API key is invalid.
            HTTPError: If the request is answered with any other error.
        """

        start = monotonic()
        response = self.get_around_client.get(
            f"https://api.watchmode.com/v1/{endpoint}",
            params={key: value for key, value in params.items() if value is not None},
            headers={"accept": "application/json", "X-API-Key": self.api_key},
        )

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError(response)
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise ResourceNotFoundError(response)

        if response.status_code != HTTPStatus.OK:
            raise HTTPError(response)

        duration = monotonic() - start
        logger.debug("Downloaded: %s - Completed in %.4f seconds", log_id, duration)

        return response.json()
