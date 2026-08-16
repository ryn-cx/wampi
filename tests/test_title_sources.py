# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_error, download_and_save, parsed_json
from wampi.exceptions import TitleNotFoundError
from wampi.title_id import resolve_title_id

if TYPE_CHECKING:
    from wampi import Wampi
    from wampi.title_sources import TitleSources

WATCHMODE_ID = 345534
IMDB_ID = "tt0903747"
TMDB_MOVIE_ID = 278
TMDB_TV_ID = 1396
INVALID_WATCHMODE_ID = 999999999

REGIONS = ["US", "CA"]
REGIONS_NAME = f"{WATCHMODE_ID} US CA"


# TODO: Validate
@pytest.fixture(scope="session")
def client(client: Wampi) -> TitleSources:
    return client.title_sources


# TODO: Validate
def test_download(client: TitleSources) -> None:
    download_and_save(
        client,
        WATCHMODE_ID,
        lambda: client.download(watchmode_id=WATCHMODE_ID),
    )


# TODO: Validate
def test_download_imdb_id(client: TitleSources) -> None:
    download_and_save(client, IMDB_ID, lambda: client.download(imdb_id=IMDB_ID))


# TODO: Validate
def test_download_tmdb_movie_id(client: TitleSources) -> None:
    download_and_save(
        client,
        resolve_title_id(tmdb_movie_id=TMDB_MOVIE_ID),
        lambda: client.download(tmdb_movie_id=TMDB_MOVIE_ID),
    )


# TODO: Validate
def test_download_tmdb_tv_id(client: TitleSources) -> None:
    download_and_save(
        client,
        resolve_title_id(tmdb_tv_id=TMDB_TV_ID),
        lambda: client.download(tmdb_tv_id=TMDB_TV_ID),
    )


# TODO: Validate
def test_download_regions(client: TitleSources) -> None:
    download_and_save(
        client,
        REGIONS_NAME,
        lambda: client.download(watchmode_id=WATCHMODE_ID, regions=REGIONS),
    )


# TODO: Validate
def test_download_invalid(client: TitleSources) -> None:
    assert_error(
        client,
        INVALID_WATCHMODE_ID,
        lambda: client.download(watchmode_id=INVALID_WATCHMODE_ID),
        TitleNotFoundError,
    )


# TODO: Validate
def test_parse(client: TitleSources) -> None:
    data = parsed_json(client, WATCHMODE_ID)
    assert data.root
    # Nothing in the response says which title it is for, so the only thing
    # that can be checked is that every source is usable.
    for source in data.root:
        assert source.source_id
        assert source.name
        assert source.region


# TODO: Validate
def test_parse_regions(client: TitleSources) -> None:
    data = parsed_json(client, REGIONS_NAME)
    assert {source.region for source in data.root} <= set(REGIONS)
