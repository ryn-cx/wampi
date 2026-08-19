from __future__ import annotations

from wampi.exceptions import TitleIdError


def _prefixed(value: str | int, prefix: str) -> str:
    """Return `value` as a string that starts with `prefix`."""
    value = str(value).strip()
    if value.startswith(prefix):
        return value
    return f"{prefix}{value}"


def _watchmode_title_id(watchmode_id: str | int) -> str:
    """Return the title id for a Watchmode id."""
    return str(watchmode_id).strip()


def _imdb_title_id(imdb_id: str) -> str:
    """Return the title id for an IMDB id, adding `tt` if it is missing."""
    return _prefixed(imdb_id, "tt")


def _tmdb_movie_title_id(tmdb_movie_id: str | int) -> str:
    """Return the title id for a TMDB movie id, adding `movie-` if it is missing."""
    return _prefixed(tmdb_movie_id, "movie-")


def _tmdb_tv_title_id(tmdb_tv_id: str | int) -> str:
    """Return the title id for a TMDB TV id, adding `tv-` if it is missing."""
    return _prefixed(tmdb_tv_id, "tv-")


# TODO: Validate
def extract_title_id(
    title_id: str | int | None = None,
    *,
    watchmode_id: str | int | None = None,
    imdb_id: str | None = None,
    tmdb_movie_id: str | int | None = None,
    tmdb_tv_id: str | int | None = None,
) -> str:
    """Extract the title id from the parameters.

    Args:
        title_id: An id that already has the required prefix.
        watchmode_id: A Watchmode id.
        imdb_id: An IMDB id with or without the `tt` prefix.
        tmdb_movie_id: A TMDB movie id with or without the `movie-` prefix.
        tmdb_tv_id: A TMDB TV id, with or without the `tv-` prefix.

    Returns:
        The title id to use as the path segment.

    Raises:
        TitleIdError: If no id or more than one id was given.
    """
    inputs: dict[str, str | int | None] = {
        "title_id": title_id,
        "watchmode_id": watchmode_id,
        "imdb_id": imdb_id,
        "tmdb_movie_id": tmdb_movie_id,
        "tmdb_tv_id": tmdb_tv_id,
    }
    title_ids = [name for name, value in inputs.items() if value is not None]
    if len(title_ids) != 1:
        raise TitleIdError(title_ids)

    if title_id is not None:
        return str(title_id).strip()
    if watchmode_id is not None:
        return _watchmode_title_id(watchmode_id)
    if imdb_id is not None:
        return _imdb_title_id(imdb_id)
    if tmdb_movie_id is not None:
        return _tmdb_movie_title_id(tmdb_movie_id)
    if tmdb_tv_id is not None:
        return _tmdb_tv_title_id(tmdb_tv_id)
    raise TitleIdError(title_ids)
