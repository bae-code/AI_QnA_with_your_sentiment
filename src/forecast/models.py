from pydantic import BaseModel, Field
from uuid import uuid4
from bson import ObjectId


class Hourly(BaseModel):
    hour: str
    weather: str
    temperature: float
    wind_speed: float
    wind_cardinal: str
    feels_like: float
    rh: float


class Forecast(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    location: str
    country: str
    date: str
    year: str
    month: str
    day: str
    hourly: list[Hourly]


class ForecastChunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    location: str
    country: str
    date: str
    range: str
    text: str
    vector_idx: int
    row_source: list[Hourly]
