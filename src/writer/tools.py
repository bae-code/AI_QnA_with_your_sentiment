from datetime import datetime
from agents import function_tool
import requests
import xmltodict
from src.config import settings


@function_tool(
    name_override="today_context",
    description_override="오늘의 날짜와 요일 정보를 반환합니다.",
)
def get_today_context() -> dict:
    info = dict()
    info["day_of_week"] = datetime.now().strftime("%A")
    info["date"] = datetime.now().strftime("%Y-%m-%d")
    return info


@function_tool(
    name_override="kr_holiday_data",
    description_override="한국의 공휴일 정보를 반환합니다.",
)
def get_kr_holiday_data() -> list[str]:
    endpoint = (
        "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    )
    year = datetime.now().year
    month = (
        datetime.now().month if datetime.now().month > 9 else f"0{datetime.now().month}"
    )
    params = {
        "solYear": year,
        "solMonth": month,
        "ServiceKey": settings.KR_GOV_DATA_API_KEY,
    }
    response = requests.get(endpoint, params=params)
    holiday_info = xmltodict.parse(response.text)

    return holiday_info


@function_tool(
    name_override="jp_holiday_data",
    description_override="일본의 공휴일 정보를 반환합니다.",
)
def get_jp_holiday_data() -> list[str]:
    endpoint = "https://holidays-jp.github.io/api/v1/date.json"

    year = datetime.now().year
    month = (
        datetime.now().month if datetime.now().month > 9 else f"0{datetime.now().month}"
    )

    response = requests.get(endpoint)
    raw_holiday_info = response.json()

    used_holiday_info = dict()
    for holiday in raw_holiday_info.keys():
        if holiday.startswith(f"{year}-{month}-"):
            used_holiday_info[holiday] = raw_holiday_info[holiday]
    return used_holiday_info


def korean_spell_check(text: str) -> str:
    return text
