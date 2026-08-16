# TODO: Validate
"""Exceptions."""

from __future__ import annotations

from typing import Any


class WampiError(Exception):
    """Base exception for Wampi."""

    response: str | dict[str, Any] | None = None


class HTTPError(WampiError):
    """Raised when HTTP request fails with unexpected status code."""

    def __init__(
        self,
        status_code: int,
        response: str | dict[str, Any] | None,
    ) -> None:
        """Initialize the HTTPError with the status code and response body."""
        self.status_code = status_code
        self.response = response
        super().__init__(f"Unexpected response status code: {status_code}")


class UnauthorizedError(HTTPError):
    """Raised when the API key is missing, invalid, or out of credits."""


class ResourceNotFoundError(HTTPError):
    """Raised when the API reports that the requested resource does not exist."""


class TitleNotFoundError(ResourceNotFoundError):
    """Raised when the requested title does not exist."""

    def __init__(
        self,
        title_id: str,
        status_code: int,
        response: str | dict[str, Any] | None,
    ) -> None:
        """Initialize with the title id and the originating response."""
        self.title_id = title_id
        super().__init__(status_code, response)


class TitleIdError(WampiError, ValueError):
    """Raised when the title being requested was not identified exactly once.

    Every id argument is optional so that any one of them can be used on its
    own, which means the check that exactly one was given has to happen at
    runtime.
    """

    def __init__(self, given: list[str]) -> None:
        """Initialize with the names of the id arguments that were given."""
        self.given = given
        if given:
            super().__init__(f"Only one title id may be given, got: {given}")
        else:
            super().__init__("A title id is required")
