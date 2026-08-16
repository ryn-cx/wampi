from good_ass_pydantic_integrator import GAPIBaseModel
from pydantic import ConfigDict, RootModel

class TitleSourcesModelItem(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    source_id: int
    name: str
    type: str
    region: str
    ios_url: str | None = None
    android_url: str | None = None
    web_url: str | None = None
    tvos_url: str | None = None
    android_tv_url: str | None = None
    roku_url: str | None = None
    format: str | None = None
    price: float | None = None
    seasons: int | None = None
    episodes: int | None = None

class TitleSourcesModel(RootModel[list[TitleSourcesModelItem]]):
    root: list[TitleSourcesModelItem]
