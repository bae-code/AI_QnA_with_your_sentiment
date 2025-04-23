from pydantic import BaseModel


class QueryPayload(BaseModel):
    location: str
    country: str
    date: str
    year: str
    month: str
    day: str


class ForecastQuery(BaseModel):
    query: QueryPayload


class WeatherSummary(BaseModel):
    temperature_summary: str
    weather_summary: str
    clothing_tips: str
    travel_tips: str
