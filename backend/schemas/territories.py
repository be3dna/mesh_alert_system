from typing import Any
from pydantic import Field, model_validator
from .common import Schema, UUIDRead

class TerritoryCreate(Schema):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    geom: dict[str, Any]  # GeoJSON geometry; converted to PostGIS by service

    @model_validator(mode="after")
    def validate_geometry_type(self):
        if self.geom.get("type") != "MultiPolygon":
            raise ValueError("geom must be a GeoJSON MultiPolygon")
        return self

class TerritoryUpdate(Schema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    geom: dict[str, Any] | None = None

class TerritoryRead(TerritoryCreate, UUIDRead):
    pass
