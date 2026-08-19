from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Self

from pydantic import BaseModel


class BaseResponseModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def from_response(cls, data: Any) -> Self:  # noqa: ANN401 - A response body can be any JSON value.
        """Return the model the response is read into."""
