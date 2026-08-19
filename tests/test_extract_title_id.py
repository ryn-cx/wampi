from __future__ import annotations

import pytest

from wampi.exceptions import TitleIdError
from wampi.extract_title_id import extract_title_id

TITLE_ID = 12345

@pytest.mark.parametrize(
    ("value", "expected"),
    [(TITLE_ID, "12345"), ("12345", "12345")],
)
def test_watchmode_id(value: str | int, expected: str) -> None:
    assert extract_title_id(watchmode_id=value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("12345", "tt12345"),
        ("tt12345", "tt12345"),
        ("0012345", "tt0012345"), # IMDB uses zero padded numbers.
        ("tt0012345", "tt0012345"),
    ],
)
def test_imdb_id(value: str, expected: str) -> None:
    assert extract_title_id(imdb_id=value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (TITLE_ID, "movie-12345"),
        ("12345", "movie-12345"),
        ("movie-12345", "movie-12345"),
    ],
)
def test_tmdb_movie_id(value: str | int, expected: str) -> None:
    assert extract_title_id(tmdb_movie_id=value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(TITLE_ID, "tv-12345"), ("12345", "tv-12345"), ("tv-12345", "tv-12345")],
)
def test_tmdb_tv_id(value: str | int, expected: str) -> None:
    assert extract_title_id(tmdb_tv_id=value) == expected


@pytest.mark.parametrize(
    "value",
    [TITLE_ID, "12345", "tt12345", "movie-12345", "tv-12345"],
)
def test_title_id(value: str | int) -> None:
    assert extract_title_id(value) == str(value)


def test_extract_title_id_without_an_id() -> None:
    with pytest.raises(TitleIdError) as exception:
        extract_title_id()
    assert exception.value.given == []


def test_extract_title_id_with_multiple_ids() -> None:
    with pytest.raises(TitleIdError) as exception:
        extract_title_id(imdb_id="tt12345", tmdb_tv_id=12345)
    assert exception.value.given == ["imdb_id", "tmdb_tv_id"]
