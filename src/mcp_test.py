import sys
import httpx

from mcp.server.fastmcp import FastMCP
from config import settings
from agents.tool import function_tool

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


accu_api_key = settings.ACCU_WEATHER_API_KEY
accu_base_url = "http://dataservice.accuweather.com/"


@function_tool(
    name_override="get_city_location_info",
    description_override="도시 이름을 입력하여 도시 위치정보를 반환하는 도구, 도시의 이름은 한글로 입력해야합니다.",
)
async def get_city_location_info(city_name: str):
    url = f"{accu_base_url}/locations/v1/cities/search"
    params = {
        "apikey": accu_api_key,
        "q": city_name,
        "language": "ko-kr",
        "details": "true",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        city_info = response.json()
        location_key = city_info[0].get("Details").get("CanonicalLocationKey")
        return location_key


@function_tool(
    name_override="get_forecast",
    description_override="위치정보와 원하는 날짜값을 입력하면 날씨 정보를 반환해줘, 날짜는 string 타입의 1,5,10,15 만 가능하고 숫자가 아니라면 가장 가까운 숫자를 찾아서 쓰세요.",
)
async def get_forecast(location_key: str, days: str):
    days = days + "day"
    url = f"{accu_base_url}/forecasts/v1/daily/{days}/{location_key}"
    params = {
        "apikey": accu_api_key,
        "locationKey": location_key,
        "language": "ko-kr",
        "details": "true",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    print("✅ MCP 서버 시작됨 (stdio 모드)", file=sys.stderr)
    # Initialize and run the server
    mcp.run(transport="stdio")
