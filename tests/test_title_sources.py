"""All TITLE_ID values are from the official documentation.

https://api.watchmode.com/docs#tag/Title/operation/getTitleSources"""

# TODO: Validate
from __future__ import annotations

from http import HTTPStatus

import pytest

from tests.utils import RecordedEndpoint
from wampi import Wampi
from wampi.exceptions import ResourceNotFoundError
from wampi.models.title_sources import TitleSources


# TODO: Validate
class WampiTest(RecordedEndpoint):
    ENDPOINT = Wampi


# TODO: Validate
class TestTitleSources:
    """Test `title_sources`."""

    class TestWatchMode(WampiTest):
        TITLE_ID = "345534"

        def test_download(self, client: Wampi) -> None:
            self.record_test(
                self.TITLE_ID,
                lambda: client.title_sources(self.TITLE_ID).raw,
            )

        def test_parse(self) -> None:
            self.parse_test(self.TITLE_ID, TitleSources)

    class TestTMDBMovie(WampiTest):
        TITLE_ID = "movie-278"

        def test_download(self, client: Wampi) -> None:
            self.record_test(
                self.TITLE_ID,
                lambda: client.title_sources(self.TITLE_ID).raw,
            )

        def test_parse(self) -> None:
            self.parse_test(self.TITLE_ID, TitleSources)

    class TestTMDBTV(WampiTest):
        TITLE_ID = "tv-1396"

        def test_download(self, client: Wampi) -> None:
            self.record_test(
                self.TITLE_ID,
                lambda: client.title_sources(self.TITLE_ID).raw,
            )

        def test_parse(self) -> None:
            self.parse_test(self.TITLE_ID, TitleSources)

    class TestIMDB(WampiTest):
        TITLE_ID = "tt0903747"

        def test_download(self, client: Wampi) -> None:
            self.record_test(
                self.TITLE_ID,
                lambda: client.title_sources(self.TITLE_ID).raw,
            )

        def test_parse(self) -> None:
            self.parse_test(self.TITLE_ID, TitleSources)

    # TODO: Validate
    class TestInvalidTitleId:
        # TODO: Validate
        @pytest.mark.parametrize("title_id", ["0", "tt00000000", "movie-0", "tv-0"])
        def test_download(self, client: Wampi, title_id: str) -> None:
            with pytest.raises(ResourceNotFoundError) as error:
                client.title_sources(title_id)

            assert error.value.response.status_code == HTTPStatus.NOT_FOUND
            assert error.value.response.json()["statusMessage"] == "Title not found"
