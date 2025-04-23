from src.core.queries import BaseQueries, Q
from src.database import forecast_collection, forecast_chunk_collection
from src.forecast.models import Forecast, ForecastChunk
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List


class ForecastQueries(BaseQueries):
    def __init__(
        self, collection: AsyncIOMotorCollection = forecast_collection
    ) -> None:
        super().__init__(collection)

    async def create_forecast(self, forecast: Forecast) -> Forecast:
        return await self.collection.insert_one(forecast.model_dump(by_alias=True))

    async def get_forecast(self, forecast_id: str) -> Forecast:
        forecast = await self.find_one(_id=forecast_id)
        return Forecast(**forecast)

    async def get_forecasts(self, **kwargs) -> List[Forecast]:
        forecasts = await self.find(**kwargs)
        return [Forecast(**forecast) for forecast in forecasts]

    async def update_forecast(self, forecast: Forecast, data: dict) -> Forecast:
        return await self.find_and_update(data=data, query=Q({"_id": forecast.id}))

    async def exists_forecast(self, **kwargs) -> bool:
        query = Q(kwargs)
        return await self.exists(query)


class ForecastChunkQueries(BaseQueries):
    def __init__(
        self, collection: AsyncIOMotorCollection = forecast_chunk_collection
    ) -> None:
        super().__init__(collection)

    async def create_forecast_chunk(
        self, forecast_chunk: ForecastChunk
    ) -> ForecastChunk:
        return await self.collection.insert_one(
            forecast_chunk.model_dump(by_alias=True)
        )

    async def get_forecast_chunks(self, **kwargs) -> List[ForecastChunk]:
        forecast_chunks = await self.find(**kwargs)
        return [ForecastChunk(**forecast_chunk) for forecast_chunk in forecast_chunks]
