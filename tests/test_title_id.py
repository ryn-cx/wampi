# TODO: Validate
from __future__ import annotations

import pytest

from wampi.exceptions import TitleIdError
from wampi.title_id import (
    imdb_title_id,
    resolve_title_id,
    tmdb_movie_title_id,
    tmdb_tv_title_id,
    watchmode_title_id,
)


# TODO: Validate
@pytest.mark.parametrize(
    ("value", "expected"),
    [(345534, "345534"), ("345534", "345534"), (" 345534 ", "345534")],
)
def test_watchmode_title_id(value: str | int, expected: str) -> None:
    assert watchmode_title_id(value) == expected


# TODO: Validate
@pytest.mark.parametrize(
    ("value", "expected"),
    [(903747, "tt903747"), ("0903747", "tt0903747"), ("tt0903747", "tt0903747")],
)
def test_imdb_title_id(value: str | int, expected: str) -> None:
    assert imdb_title_id(value) == expected


# TODO: Validate
@pytest.mark.parametrize(
    ("value", "expected"),
    [(278, "movie-278"), ("278", "movie-278"), ("movie-278", "movie-278")],
)
def test_tmdb_movie_title_id(value: str | int, expected: str) -> None:
    assert tmdb_movie_title_id(value) == expected


# TODO: Validate
@pytest.mark.parametrize(
    ("value", "expected"),
    [(1396, "tv-1396"), ("1396", "tv-1396"), ("tv-1396", "tv-1396")],
)
def test_tmdb_tv_title_id(value: str | int, expected: str) -> None:
    assert tmdb_tv_title_id(value) == expected


# TODO: Validate
def test_resolve_title_id_is_used_as_is() -> None:
    # An id that is passed positionally already carries its prefix, so nothing
    # is added to it even when it looks like an id of another kind.
    assert resolve_title_id("tv-1396") == "tv-1396"
    assert resolve_title_id(1396) == "1396"


# TODO: Validate
@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        ({"watchmode_id": 345534}, "345534"),
        ({"imdb_id": 903747}, "tt903747"),
        ({"tmdb_movie_id": 278}, "movie-278"),
        ({"tmdb_tv_id": 1396}, "tv-1396"),
    ],
)
def test_resolve_title_id_adds_the_prefix(
    kwargs: dict[str, int],
    expected: str,
) -> None:
    assert resolve_title_id(**kwargs) == expected


# TODO: Validate
def test_resolve_title_id_without_an_id() -> None:
    with pytest.raises(TitleIdError) as excinfo:
        resolve_title_id()
    assert excinfo.value.given == []


# TODO: Validate
def test_resolve_title_id_with_two_ids() -> None:
    with pytest.raises(TitleIdError) as excinfo:
        resolve_title_id(imdb_id="tt0903747", tmdb_tv_id=1396)
    assert excinfo.value.given == ["imdb_id", "tmdb_tv_id"]
