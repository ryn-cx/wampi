# TODO: Validate
"""Contains BaseEndpoint."""

from __future__ import annotations

from abc import abstractmethod
from inspect import Parameter, signature
from typing import TYPE_CHECKING, Any

from good_ass_pydantic_integrator import GAPIClient
from pydantic import BaseModel

from wampi.constants import FILES_PATH

if TYPE_CHECKING:
    from collections.abc import Callable

    from wampi import Wampi


# TODO: Validate
class BaseEndpoint[T: BaseModel, **P = ...](GAPIClient[T]):
    """Base class for API endpoints."""

    JSON_FILES_ROOT = FILES_PATH

    # TODO: Validate
    def __init__(self, client: Wampi) -> None:
        """Initialize the endpoint with the Wampi client."""
        self._client = client

    # TODO: Validate
    @staticmethod
    def non_default_args(
        func: Callable[..., Any],
        values: dict[str, Any],
    ) -> dict[str, Any]:
        """Return the args that are changed from their default values."""
        return {
            name: values[name]
            for name, param in signature(func).parameters.items()
            if param.default is not Parameter.empty
            and name in values
            and values[name] != param.default
        }

    # TODO: Validate
    def get_log_id(self, func: Callable[..., Any], values: dict[str, Any]) -> str:
        """Gets the log id.

        Example: ClassName (arg1='value1' arg2='value2')
        """
        required = {
            name: values[name]
            for name, param in signature(func).parameters.items()
            if param.default is Parameter.empty and name in values
        }
        set_args = {**required, **self.non_default_args(func, values)}
        parts = [
            *(f"{name}={value!r}" for name, value in set_args.items()),
        ]
        name = self.__class__.__name__
        if not parts:
            return name
        return f"{name} ({' '.join(parts)})"

    # TODO: Validate
    @abstractmethod
    def download(self, *args: P.args, **kwargs: P.kwargs) -> list[dict[str, Any]]:
        """Downloads the file."""

    # TODO: Validate
    @abstractmethod
    def download_and_parse(self, *args: P.args, **kwargs: P.kwargs) -> T:
        """Downloads and parses the file."""
