# TODO: Validate
"""Helpers that build the title id the API takes.

Watchmode identifies a title by a single path segment that is either a plain
Watchmode id, an IMDB id, or a TMDB id prefixed with the type it belongs to.
Every endpoint takes both the ready made id and the individual ids, so these
helpers add the prefix that a bare id is missing while leaving an id that
already carries it alone.
"""

from __future__ import annotations

from wampi.exceptions import TitleIdError

IMDB_PREFIX = "tt"
"""Prefix of every IMDB id."""

TMDB_MOVIE_PREFIX = "movie-"
"""Prefix Watchmode uses for a TMDB movie id."""

TMDB_TV_PREFIX = "tv-"
"""Prefix Watchmode uses for a TMDB TV id."""


# TODO: Validate
def _prefixed(value: str | int, prefix: str) -> str:
    """Return `value` as a string that starts with `prefix`."""
    value = str(value).strip()
    if value.startswith(prefix):
        return value
    return f"{prefix}{value}"


# TODO: Validate
def watchmode_title_id(watchmode_id: str | int) -> str:
    """Return the title id for a Watchmode id.

    A Watchmode id carries no prefix, so this only normalizes it to a string.
    """
    return str(watchmode_id).strip()


# TODO: Validate
def imdb_title_id(imdb_id: str | int) -> str:
    """Return the title id for an IMDB id, adding `tt` if it is missing."""
    return _prefixed(imdb_id, IMDB_PREFIX)


# TODO: Validate
def tmdb_movie_title_id(tmdb_movie_id: str | int) -> str:
    """Return the title id for a TMDB movie id, adding `movie-` if it is missing."""
    return _prefixed(tmdb_movie_id, TMDB_MOVIE_PREFIX)


# TODO: Validate
def tmdb_tv_title_id(tmdb_tv_id: str | int) -> str:
    """Return the title id for a TMDB TV id, adding `tv-` if it is missing."""
    return _prefixed(tmdb_tv_id, TMDB_TV_PREFIX)


# TODO: Validate
def resolve_title_id(
    title_id: str | int | None = None,
    *,
    watchmode_id: str | int | None = None,
    imdb_id: str | int | None = None,
    tmdb_movie_id: str | int | None = None,
    tmdb_tv_id: str | int | None = None,
) -> str:
    """Return the single title id that the given arguments identify.

    Args:
        title_id: An id that already carries whatever prefix it needs, used
            without adding one.
        watchmode_id: A Watchmode id, which takes no prefix.
        imdb_id: An IMDB id, prefixed with `tt` if it is missing.
        tmdb_movie_id: A TMDB movie id, prefixed with `movie-` if it is missing.
        tmdb_tv_id: A TMDB TV id, prefixed with `tv-` if it is missing.

    Returns:
        The title id to use as the path segment.

    Raises:
        TitleIdError: If no id or more than one id was given.
    """
    given = {
        "title_id": title_id,
        "watchmode_id": watchmode_id,
        "imdb_id": imdb_id,
        "tmdb_movie_id": tmdb_movie_id,
        "tmdb_tv_id": tmdb_tv_id,
    }
    used = [name for name, value in given.items() if value is not None]
    if len(used) != 1:
        raise TitleIdError(used)

    if title_id is not None:
        return str(title_id).strip()
    if watchmode_id is not None:
        return watchmode_title_id(watchmode_id)
    if imdb_id is not None:
        return imdb_title_id(imdb_id)
    if tmdb_movie_id is not None:
        return tmdb_movie_title_id(tmdb_movie_id)
    if tmdb_tv_id is not None:
        return tmdb_tv_title_id(tmdb_tv_id)
    raise TitleIdError(used)
