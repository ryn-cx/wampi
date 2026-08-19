# TODO: Validate
"""Title Sources models."""

from __future__ import annotations

from typing import Any, Self, override

from pydantic import BaseModel, ConfigDict, Field, SkipValidation

from wampi.base_response_model import BaseResponseModel


# TODO: Validate
class Source(BaseModel):
    """One place a title can be watched.

    The per-platform deep links are not read: they are only filled in for paid
    plans and every one of them points at the same title as `url`. They stay in
    the response either way.

    Attributes:
        id: What the API knows this source by.
        name: The service, as it is written for a person to read.
        type: How it is paid for: `sub`, `free`, `purchase`, `tve` or `rent`.
        region: The two letter country code the source is available in.
        url: Where the title is on that service, on the web.
        format: The best quality it is carried in, such as `HD` or `4K`, or
            None when the source does not say.
        price: What it costs to buy or rent, or None when it is not sold that
            way.
        seasons: How many seasons the source carries, for a TV show only.
        episodes: How many episodes the source carries, for a TV show only.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    source_id: int
    name: str
    type: str
    region: str
    web_url: str
    format: str | None
    price: float | None
    seasons: int | None
    episodes: int | None


# TODO: Validate
class TitleSources(BaseResponseModel):
    """Everywhere one title can be watched.

    Nothing in the response says which title it is for, so what came back is
    only the sources themselves.

    Attributes:
        sources: Every source the title is currently available from.
        raw: The response as it was downloaded.
    """

    model_config = ConfigDict(frozen=True)

    sources: tuple[Source, ...]
    raw: SkipValidation[list[dict[str, Any]]] = Field(repr=False)

    # TODO: Validate
    @classmethod
    @override
    def from_response(cls, data: list[dict[str, Any]]) -> Self:
        return cls.model_validate({"sources": data, "raw": data})
