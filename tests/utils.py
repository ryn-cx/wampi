# TODO: Validate
"""Utils."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Literal, overload

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from typing import Any

    from good_ass_pydantic_integrator import GAPIClient
    from pydantic import BaseModel

    from wampi.base_api_endpoint import BaseEndpoint
    from wampi.exceptions import WampiError


_INVALID_FILE_NAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
"""Characters Windows does not allow in a file name."""

_RESERVED_FILE_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(1, 10)}
    | {f"LPT{i}" for i in range(1, 10)},
)
"""Device names Windows reserves and cannot be used as a file name."""


# TODO: Validate
def sanitized_file_name(name: str | int) -> str:
    """Turn a name into a file name that is valid on Windows.

    Invalid characters are replaced with an underscore, trailing dots and spaces
    are stripped because Windows silently drops them, and reserved device names
    are suffixed so they stay usable.
    """
    sanitized = _INVALID_FILE_NAME_CHARS.sub("_", str(name)).rstrip(". ")
    if not sanitized:
        return "_"
    if sanitized.partition(".")[0].upper() in _RESERVED_FILE_NAMES:
        return f"{sanitized}_"
    return sanitized


# TODO: Validate
def json_path(
    gapi_client: GAPIClient[Any],
    name: str | int,
    category: Literal["Multipage", "Error"] | None = None,
) -> Path:
    file_name = f"{sanitized_file_name(name)}.json"
    if category:
        return (
            gapi_client.json_files_folder().parent
            / (category + "s")
            / gapi_client.json_files_folder().stem
            / file_name
        )

    return gapi_client.json_files_folder() / file_name


# TODO: Validate
def json_content[T: BaseModel](
    gapi_client: BaseEndpoint[T, ...],
    name: str | int,
    category: Literal["Multipage", "Error"] | None = None,
) -> str:
    return json_path(gapi_client, name, category=category).read_text()


# TODO: Validate
def loaded_json(
    gapi_client: BaseEndpoint[Any, ...],
    name: str | int,
    category: Literal["Multipage"] | None = None,
) -> dict[str, Any]:
    return json.loads(json_content(gapi_client, name, category=category))


# TODO: Validate
@overload
def parsed_json[T: BaseModel](
    gapi_client: BaseEndpoint[T, ...],
    name: str | int,
    category: Literal["Multipage"],
) -> list[T]: ...
# TODO: Validate
@overload
def parsed_json[T: BaseModel](
    gapi_client: BaseEndpoint[T, ...],
    name: str | int,
    category: None = None,
) -> T: ...
# TODO: Validate
def parsed_json[T: BaseModel](
    gapi_client: BaseEndpoint[T, ...],
    name: str | int,
    category: Literal["Multipage"] | None = None,
) -> T | list[T]:
    data = json.loads(json_content(gapi_client, name, category=category))
    if category == "Multipage":
        return [gapi_client.parse(page) for page in data]
    return gapi_client.parse(data)


# TODO: Validate
def download_and_save(
    gapi_client: GAPIClient[Any],
    name: str | int,
    get: Callable[[], dict[str, Any] | list[dict[str, Any]]],
    category: Literal["Multipage"] | None = None,
) -> Path:
    file = json_path(gapi_client, name, category)
    if file.exists():
        msg = f"File already recorded for {type(gapi_client).__name__}/{name}"
        pytest.skip(msg)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(get(), indent=2))
    return file


# TODO: Validate
def assert_error(
    gapi_client: GAPIClient[Any],
    name: str | int,
    download: Callable[[], object],
    error: type[WampiError],
) -> None:
    if json_path(gapi_client, name, "Error").exists():
        msg = f"File already recorded for {type(gapi_client).__name__}/{name}"
        pytest.skip(msg)
    with pytest.raises(error) as excinfo:
        download()
    record_error(gapi_client, name, excinfo.value.response)


# TODO: Validate
def get_error_path(gapi_client: GAPIClient[Any], name: str | int) -> Path:
    return json_path(gapi_client, name, category="Error")


# TODO: Validate
def record_error(
    gapi_client: GAPIClient[Any],
    name: str | int,
    response: str | dict[str, Any] | None = None,
) -> None:
    json_path = get_error_path(gapi_client, name)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    if response is None:
        content = ""
    elif isinstance(response, str):
        content = response
    else:
        content = json.dumps(response, indent=2)
    json_path.write_text(content)
