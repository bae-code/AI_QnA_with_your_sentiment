import httpx
from datetime import datetime
from src.forecast.queries import ForecastQueries, ForecastChunkQueries
from src.forecast.models import Forecast, Hourly, ForecastChunk
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import numpy as np


tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-small")
model = AutoModel.from_pretrained("intfloat/multilingual-e5-small")


def get_embedding(text: str) -> list[float]:
    encoded_input = tokenizer(
        f"query: {text}", return_tensors="pt", truncation=True, padding=True
    )
    with torch.no_grad():
        model_output = model(**encoded_input)
    return model_output.last_hidden_state[:, 0, :][0].cpu().numpy()


forecast_queries = ForecastQueries()
forecast_chunk_queries = ForecastChunkQueries()


async def parse_weather_data() -> None:
    forecasts = await forecast_queries.get_forecasts(location="sapporo", country="jp")
    dim = 384
    index = faiss.IndexFlatL2(dim)
    index = faiss.IndexIDMap2(index)  # ≤‑‑‑ 사용자‑지정 ID 부여
    for forecast in forecasts:
        title = (
            f"{forecast.id} {forecast.location}({forecast.country}) {forecast.date} 일"
        )
        docs = ""

        # 6시간 단위로 쪼개기

        for i in range(0, len(forecast.hourly), 6):
            hourly_data = forecast.hourly[i : i + 6]

            title = f"date: {forecast.date}|location: {forecast.location}|country: {forecast.country}|range: {i}시 ~ {i + 5}시"

            docs = ""

            for hourly in hourly_data:
                docs += f"{hourly.hour}시: 날씨는 {hourly.weather}, 기온은 {hourly.temperature}도, 풍속은 {hourly.wind_speed}m/s, 풍향은 {hourly.wind_cardinal}, 체감온도는 {hourly.feels_like}도, 습도는 {hourly.rh}% 입니다.\n"

            result = title + "|" + docs
            embedding = get_embedding(result).astype(np.float32)

            vec_id = np.int64(f"{forecast.date.replace('-', '')}{i:02d}")
            forecast_chunk = ForecastChunk(
                location=forecast.location,
                country=forecast.country,
                date=forecast.date,
                range=f"{i}시 ~ {i + 5}시",
                text=result,
                vector_idx=vec_id,
                row_source=hourly_data,
            )

            index.add_with_ids(
                np.expand_dims(embedding, axis=0),  # shape (1, 384)
                np.expand_dims(vec_id, axis=0),  # shape (1,)
            )

            await forecast_chunk_queries.create_forecast_chunk(forecast_chunk)
            # 저장
    faiss.write_index(index, "weather_index.faiss")


def parse_query(q: str) -> tuple[str, str, int, int]:
    # "20240401 삿포로 오전 6시 ~ 오전 11시 날씨 정보"
    date, loc, h_from, h_to = q.split(" ")
    return date, loc, int(h_from), int(h_to)


async def get_faiss_test():
    # 불러오기
    index = faiss.read_index("weather_index.faiss")

    user_query = "20240401 sapporo 06 11"
    date, loc, h_from, h_to = parse_query(user_query)
    forecast_chunks = await forecast_chunk_queries.get_forecast_chunks(
        date=date, location=loc, range=f"{h_from}시 ~ {h_to}시"
    )

    subset_ids = [doc.vector_idx for doc in forecast_chunks]

    if not subset_ids:
        return "해당 구간 데이터가 없어요!"

    selector = faiss.IDSelectorBatch(np.array(subset_ids, dtype="int64"))
    params = faiss.SearchParameters()
    params.sel = selector

    q_vec = get_embedding(user_query).reshape(1, -1)
    D, I = index.search(q_vec, k=1, params=params)
    print(forecast_chunks[int(I[0][0])].text)
    return forecast_chunks[int(I[0][0])].text


async def get_weather_data(country: str, location: str, date: str, url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        data = response.json()

        try:
            weather_data = data["observations"]
        except:
            print(f"{location} {country} {date} is not found")
            return

        if await forecast_queries.exists_forecast(
            location=location, country=country, date=date
        ):
            print(f"{location} {country} {date} is already exists")
            return

        forecast = Forecast(
            location=location,
            country=country,
            date=date,
            year=date[:4],
            month=date[4:6],
            day=date[6:],
            hourly=[],
        )

        for i in weather_data:
            wx_phrase = i["wx_phrase"] or "unknown"  # 날씨 상태
            temp = i["temp"] or 0  # 온도 (화씨)
            wind_speed = i["wspd"] or 0  # 바람 세기
            wind_cardinal = i["wdir_cardinal"] or "unknown"  # 바람 방향
            feels_like = i["feels_like"] or 0  # 체감 온도 (화씨)
            rh = i["rh"] or 0  # 습기
            time = i["valid_time_gmt"]
            time = datetime.fromtimestamp(time)
            hour_data = Hourly(
                hour=time.strftime("%H"),
                weather=wx_phrase,
                temperature=change_fahrenheit_to_celsius(temp),
                wind_speed=wind_speed,
                wind_cardinal=wind_cardinal,
                feels_like=change_fahrenheit_to_celsius(feels_like),
                rh=rh,
            )

            forecast.hourly.append(hour_data)

        await forecast_queries.create_forecast(forecast)
        return data


def change_fahrenheit_to_celsius(fahrenheit: float) -> float:
    return int(round((fahrenheit - 32.00) * (5.00 / 9.00), 0))
