# TODO: Validate
"""Watchmode title sources API.

The client holds every endpoint the API answers and the single download all of
them go through. An endpoint is a method rather than an object of its own, so
`client.title_sources("345534")` is `title/345534/sources` and is the whole of
it: no download is asked for and then parsed, because the method does both.
"""

from __future__ import annotations

from http import HTTPStatus
from logging import NullHandler, getLogger
from time import monotonic
from typing import TYPE_CHECKING, Any, overload

from get_around import GetAround

from wampi._log_id import get_log_id
from wampi.exceptions import (
    HTTPError,
    ResourceNotFoundError,
    UnauthorizedError,
)
from wampi.extract_title_id import extract_title_id
from wampi.models.title_sources import TitleSources

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = getLogger(__name__)
logger.addHandler(NullHandler())


# TODO: Validate
class Wampi:
    """Watchmode title sources API wrapper."""

    # TODO: Validate
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

    # TODO: Validate
    @overload
    def title_sources(
        self,
        title_id: str | int,
        *,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    # TODO: Validate
    @overload
    def title_sources(
        self,
        *,
        watchmode_id: str | int,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    # TODO: Validate
    @overload
    def title_sources(
        self,
        *,
        imdb_id: str,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    # TODO: Validate
    @overload
    def title_sources(
        self,
        *,
        tmdb_movie_id: str | int,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    # TODO: Validate
    @overload
    def title_sources(
        self,
        *,
        tmdb_tv_id: str | int,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    # TODO: Validate
    def title_sources(  # noqa: PLR0913 - Extra parameters make it easier for the caller.
        self,
        title_id: str | int | None = None,
        *,
        watchmode_id: str | int | None = None,
        imdb_id: str | None = None,
        tmdb_movie_id: str | int | None = None,
        tmdb_tv_id: str | int | None = None,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources:
        """Get title streaming sources .

        Get all streaming sources where a title is currently available. Returns
        subscription services, rental options, purchase options, and free streaming.
        For TV shows, includes information about available seasons and episodes per
        source.

        Args:
            title_id: Title identifier. Accepts:
                Watchmode ID (e.g., 345534) - 1 credit
                IMDB ID (e.g., tt0903747) - 2 credits
                TMDB format (e.g., movie-278 or tv-1396) - 2 credits

            watchmode_id: Watchmode ID (e.g., 345534) - 1 credit.
            imdb_id: IMDB ID (e.g., tt0903747 or 0903747) - 2 credits. It is a
                string only, because the id is zero padded and a number drops
                the padding.
            tmdb_movie_id: TMDB movie format (e.g., movie-278 or 278) - 2 credits
            tmdb_tv_id: TMDB tv format (e.g., tv-1396 or 1396) - 2 credits
            regions:  Example: regions=US,CA

                Filter by region (2-letter country code). Comma-separated for multiple.
                Requested regions must be enabled for your plan. If omitted, returns
                sources from regions enabled for your plan.


        Raises:
            TitleIdError: If no id or more than one id was given.
            ResourceNotFoundError: If the title does not exist.
        """
        log_id = get_log_id(self.title_sources, locals())
        title_id = extract_title_id(
            title_id,
            watchmode_id=watchmode_id,
            imdb_id=imdb_id,
            tmdb_movie_id=tmdb_movie_id,
            tmdb_tv_id=tmdb_tv_id,
        )
        if regions is not None and not isinstance(regions, str):
            regions = ",".join(regions)

        data = self.download(
            endpoint=f"title/{title_id}/sources/",
            params={"regions": regions},
            log_id=log_id,
        )

        return TitleSources.from_response(data)

    # TODO: Validate
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
