"""Get title streaming sources .

Get all streaming sources where a title is currently available. Returns subscription
services, rental options, purchase options, and free streaming. For TV shows, includes
information about available seasons and episodes per source.
"""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import TYPE_CHECKING, overload

from wampi.base_endpoint import BaseEndpoint
from wampi.extract_title_id import extract_title_id
from wampi.title_sources.models import TitleSources

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class GetTitleSources(BaseEndpoint):
    """Get title streaming sources .

    Get all streaming sources where a title is currently available. Returns subscription
    services, rental options, purchase options, and free streaming. For TV shows, includes
    information about available seasons and episodes per source.
    """

    @overload
    def fetch(
        self,
        title_id: str | int,
        *,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    @overload
    def fetch(
        self,
        *,
        watchmode_id: str | int,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    @overload
    def fetch(
        self,
        *,
        imdb_id: str,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    @overload
    def fetch(
        self,
        *,
        tmdb_movie_id: str | int,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    @overload
    def fetch(
        self,
        *,
        tmdb_tv_id: str | int,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSources: ...

    def fetch(  # noqa: PLR0913 - Extra parameters make it easier for the caller.
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
        log_id = self.get_log_id(self.fetch, locals())
        title_id = extract_title_id(
            title_id,
            watchmode_id=watchmode_id,
            imdb_id=imdb_id,
            tmdb_movie_id=tmdb_movie_id,
            tmdb_tv_id=tmdb_tv_id,
        )
        if regions is not None and not isinstance(regions, str):
            regions = ",".join(regions)

        data = self._client.download(
            endpoint=f"title/{title_id}/sources/",
            params={"regions": regions},
            log_id=log_id,
        )

        return TitleSources.from_response(data)
