from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx


class WampiError(Exception):
    """Base exception for Wampi."""


class HTTPError(WampiError):
    """Raised when an HTTP request fails with an unexpected status code."""

    response: httpx.Response
    """The response that caused the error, request included."""

    # TODO: Validate
    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        super().__init__(
            f"Unexpected response status code: {response.status_code}\n{response.text}",
        )


class UnauthorizedError(HTTPError):
    """Raised when the API key is missing, invalid, or out of credits."""


class ResourceNotFoundError(HTTPError):
    """Raised when the API reports that the requested resource does not exist."""


class TitleIdError(WampiError, ValueError):
    """Raised when the title_id cannot be determined."""

    def __init__(self, title_ids: list[str]) -> None:
        self.inputs_with_values = title_ids
        if title_ids:
            super().__init__(f"Only one title id may be given, got: {title_ids}")
        else:
            super().__init__("A title id is required")
