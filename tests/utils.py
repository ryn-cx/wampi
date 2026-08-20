# TODO: Validate
"""Helpers shared by every endpoint's tests.

Nothing here knows about a particular endpoint. What an endpoint's own test file
brings is the ids it downloads, the class it parses into and what it expects to
find; recording a response and reading it back is the same either way.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from wampi.base_response_model import BaseResponseModel


# TODO: Validate
class RecordedEndpoint:
    """Reads and writes the recordings a test class owns.

    What tells two recordings of one endpoint apart is the test that asked for
    them rather than anything in the request, since every test of an endpoint
    asks for the same thing under a different set of arguments. Subclassing is
    what says which test that is: the recordings live under the subclass's own
    name, so nothing has to be told the name or carry it around.

    Never put a `test_` method here. It would be inherited and so would run once
    per subclass.
    """

    ENDPOINT: ClassVar[type]
    """The endpoint whose responses the subclass records."""

    # TODO: Validate
    @classmethod
    def _recording_path(cls, folder: str, name: str | int) -> Path:
        """Return the path a recording of `name` is kept at.

        A test class is nested inside the endpoint it covers, so its qualified
        name already says which endpoint answered and which case was asked for.
        The recording is filed under that nesting rather than under the class
        name alone, which two endpoints are free to share.

        What a recording is named after is as often a number as a string, so
        `name` is taken as either and written out as a string here rather than
        at every call.
        """
        root = Path(__file__).parent / folder / cls.ENDPOINT.__name__
        return root.joinpath(*cls.__qualname__.split(".")) / f"{name}.json"

    # TODO: Validate
    @classmethod
    def recorded_file_path(cls, name: str | int) -> Path:
        """Return the path of the recorded file."""
        return cls._recording_path("_files", name)

    # TODO: Validate
    @classmethod
    def recorded_content(cls, name: str | int) -> list[dict[str, Any]]:
        """Return the content of the recorded file."""
        path = cls.recorded_file_path(name)
        if not path.exists():
            pytest.skip(f"No recorded response for {name}")
        content: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
        return content

    # TODO: Validate
    @classmethod
    def new_file_path(cls, name: str | int) -> Path:
        """Return the path a response that does not match its recording is put."""
        return cls._recording_path("_new_files", name)

    # TODO: Validate
    @classmethod
    def record_test(
        cls,
        name: str | int,
        download: Callable[[], list[dict[str, Any]]],
    ) -> None:
        """Download a response and check it against what was recorded.

        Writing a recording fails the test rather than skipping it, because what
        was just written is only whatever the API happened to answer: it has to
        be read before it can stand in for correct.

        A response that does not match its recording is written to `_new_files`
        and the test fails. The recording is left alone, so the two can be
        diffed and the new one moved over the old one once it has been looked
        at.
        """
        path = cls.recorded_file_path(name)
        downloaded = download()

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(downloaded, indent=2), encoding="utf-8")
            pytest.fail(f"No recorded response for {name}, so it was recorded now")

        new_path = cls.new_file_path(name)
        if downloaded != json.loads(path.read_text(encoding="utf-8")):
            new_path.parent.mkdir(parents=True, exist_ok=True)
            new_path.write_text(json.dumps(downloaded, indent=2), encoding="utf-8")
            pytest.fail(f"Response for {name} is not what was recorded, see {new_path}")

        # What is in `_new_files` is whatever last failed to match, so a response
        # that matches again clears it rather than leaving a stale mismatch
        # behind.
        new_path.unlink(missing_ok=True)

    # TODO: Validate
    @classmethod
    def recorded_model_path(cls, name: str | int) -> Path:
        """Return the path of the recorded model dump."""
        return cls._recording_path("_models", name)

    # TODO: Validate
    @classmethod
    def recorded_model_content(
        cls,
        name: str | int,
        model: BaseResponseModel,
    ) -> dict[str, Any]:
        """Return the recorded dump of `model`, writing the recording the first time.

        A parse test compares what it read against this rather than against a
        model it builds from the same response, because a model built from the
        response mirrors whatever the reading does and cannot disagree with it.

        What is returned is the recording as it stands rather than a model read
        back out of it, since reading it back puts it through the same coercion
        the parsing does and so hides a value that is written one way and read
        another.

        Writing a recording fails the test rather than skipping it, because what
        was just written is only whatever the reading currently produces: it is
        the thing being checked and has to be read before it can stand in for
        correct.
        """
        path = cls.recorded_model_path(name)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(model.model_dump(mode="json"), indent=2),
                encoding="utf-8",
            )
            pytest.fail(f"No recorded model for {name}, so it was recorded now")
        content: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        return content

    # TODO: Validate
    @classmethod
    def parse_test(cls, name: str | int, model: type[BaseResponseModel]) -> None:
        """Read a recorded response and check it against the recorded model.

        The reading is the model's own `from_response`, which is what a download
        ends in too, so the test exercises the same call.

        What the two sides are compared as is what each is written out to rather
        than as models, so what is checked is every value as it is recorded
        rather than two models that agree only because reading the recording
        back undid whatever the parsing did to it.
        """
        parsed = model.from_response(cls.recorded_content(name))
        recorded = cls.recorded_model_content(name, parsed)

        assert parsed.model_dump(mode="json") == recorded
