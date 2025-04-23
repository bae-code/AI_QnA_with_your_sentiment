import requests
from agents import function_tool
from src.forecast.schemas import WeatherSummary
from src.config import settings


@function_tool(
    name_override="find_fore_cast_with_perplexity",
    description_override="Use web search to find daily high/low °C, weather condition, and precipitation for the requested city and date range; return exactly in the provided JSON response schema without any extra text.",
)
def find_fore_cast_with_perplexity(user_request: str):
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": "Use web search to find daily high/low °C, weather condition, and precipitation for the requested city and date range; return exactly in the provided JSON response schema without any extra text.",
            },
            {
                "role": "user",
                "content": user_request,
            },
        ],
        "max_tokens": 4244,
        "temperature": 0.2,
        "top_p": 0.9,
        "search_domain_filter": [
            "meteum.ai",
            "weather25.com",
            "accuweather.com",
            "weather.com",
            "jma.go.jp",
            "timeanddate.com",
            "meteostat.net",
            "yr.no",
            "triple.guide",
        ],
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": WeatherSummary.model_json_schema()},
        },
        "web_search_options": {"search_context_size": "high"},
    }
    headers = {
        "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = response.json()

    return data["choices"][0]["message"]["content"]
