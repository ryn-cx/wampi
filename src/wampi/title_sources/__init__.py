# TODO: Validate
"""Contains the TitleSources class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import TYPE_CHECKING, Any, override

from wampi.base_api_endpoint import BaseEndpoint
from wampi.exceptions import ResourceNotFoundError, TitleNotFoundError
from wampi.title_id import resolve_title_id
from wampi.title_sources.models import TitleSourcesModel

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = getLogger(__name__)
logger.addHandler(NullHandler())


# TODO: Validate
class TitleSources(BaseEndpoint[TitleSourcesModel]):
    """Manage the title sources file.

    Every source a title is currently available from, which covers
    subscription, rental, purchase, free and TV channel app availability. For a
    TV show a source also reports how many seasons and episodes it carries.

    Wraps `GET /v1/title/{title_id}/sources/`:
    https://api.watchmode.com/docs#tag/Title/operation/getTitleSources

    The title is identified either by `title_id`, which is used exactly as it
    is given, or by one of the individual ids, which get the prefix Watchmode
    expects added for them. Exactly one of them must be given. An IMDB or TMDB
    id costs two API credits, a Watchmode id costs one.
    """

    _response_model = TitleSourcesModel

    # TODO: Validate
    @override
    def download(
        self,
        title_id: str | int | None = None,
        *,
        watchmode_id: str | int | None = None,
        imdb_id: str | int | None = None,
        tmdb_movie_id: str | int | None = None,
        tmdb_tv_id: str | int | None = None,
        regions: str | Sequence[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Downloads the title sources file.

        Args:
            title_id: A title id that already carries whatever prefix it needs,
                for example `345534`, `tt0903747` or `movie-278`.
            watchmode_id: A Watchmode id, which takes no prefix.
            imdb_id: An IMDB id, prefixed with `tt` if it is missing.
            tmdb_movie_id: A TMDB movie id, prefixed with `movie-` if missing.
            tmdb_tv_id: A TMDB TV id, prefixed with `tv-` if missing.
            regions: Two letter country codes to limit the sources to, either
                comma separated or as a sequence. Defaults to every region the
                API key is enabled for.

        Returns:
            The sources as they were downloaded.

        Raises:
            TitleIdError: If no id or more than one id was given.
            TitleNotFoundError: If the title does not exist.
        """
        log_id = self.get_log_id(self.download, locals())
        resolved_id = resolve_title_id(
            title_id,
            watchmode_id=watchmode_id,
            imdb_id=imdb_id,
            tmdb_movie_id=tmdb_movie_id,
            tmdb_tv_id=tmdb_tv_id,
        )
        if not isinstance(regions, str) and regions is not None:
            regions = ",".join(regions)

        try:
            return self._client.download(
                # The trailing slash is what the documented URL uses.
                endpoint=f"title/{resolved_id}/sources/",
                params={"regions": regions},
                log_id=log_id,
            )
        except ResourceNotFoundError as err:
            raise TitleNotFoundError(
                resolved_id,
                err.status_code,
                err.response,
            ) from err

    # TODO: Validate
    @override
    def download_and_parse(
        self,
        title_id: str | int | None = None,
        *,
        watchmode_id: str | int | None = None,
        imdb_id: str | int | None = None,
        tmdb_movie_id: str | int | None = None,
        tmdb_tv_id: str | int | None = None,
        regions: str | Sequence[str] | None = None,
    ) -> TitleSourcesModel:
        """Downloads and parses the title sources file."""
        return self.parse(
            self.download(
                title_id,
                watchmode_id=watchmode_id,
                imdb_id=imdb_id,
                tmdb_movie_id=tmdb_movie_id,
                tmdb_tv_id=tmdb_tv_id,
                regions=regions,
            ),
        )
