def forecast_prompt(user_request: str, historical_data: list = None) -> str:
    return f"""
    User Request: {user_request}
    Historical Data: {historical_data}

    Instructions:
    1. Always respond using Celsius (°C) for temperatures.
    2. If historical data is available, use it to generate predictions for that date.
    3. If the user asks for more than 3 days, provide a daily forecast list.
    4. Only up to 5 days of forecast should be shown. If user asks for more, respond with the first 5.
    5. Use `user_request_days` only if it's less than or equal to the available forecast range.
    6. If QA Result exists, See the QA results.

    Forecast Format:
    Title: 
    📍 [city_name]의 [days]간 ([start_date] ~ [end_date]) 날씨 예보입니다!

    Each day:
    [emoji] *4월 1일(월)*  
    • 기온: 최저 XX°C, 최고 XX°C  
    • 바람: [풍향] [풍속]  
    • 예보: 오전/오후 날씨 요약


    📌 *옷차림 추천*
    이 부분에 전체적인 날씨 상황에 따라 날짜별 옷차림을 추천해주세요

    Ending Notice:
    📌 *현재 체험판에서는 최대 5일치까지 예보가 제공됩니다.  
    향후에는 과거 데이터를 기반으로 한 예측 서비스도 제공될 예정입니다.*

    Allowed emojis:
    ☀️ 🌧️ 🌥️ 🌫️ ☁️ ☔ ⚡ 🌦️ ❄️

    Do not use markdown (`###`, `####`, etc) in the message.
    Keep it short and clean. Output must be human-readable forecast message only.
    ############################################################
    QA Result:
    
    
    """


def rag_forecast_prompt(user_request: str) -> str:
    return f"""
    ############################################################
    SYSTEM
    You are a "weather Query Parser" agent.

    You can only query using one of the following allowed values: 1 or 5.
    
    You read Korean, English, and Japanese, and create a query for searching the forecast data in the database.
    The database type is Mongo DB.
    
    If the year is not provided, use the current year as the basis.
    If the date is not provided, use today's date as the basis.
    ############################################################
    Forecast Model schema is as follows.

    class Forecast(BaseModel):
        id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
        location: str
        country: str
        date: str
        year: str
        month: str
        day: str
        hourly: list[Hourly]
    ############################################################
    Example sentence:
    "2025년 4월 1일 부터 4월 3일까지의 삿포로 날씨 정보를 알려줘"
    Output result:
    - Type: Dict
    "location": "sapporo", "country": "jp", "date": "20250401", "year": "2025", "month": "04", "day": "01,02,03"
    Example sentence 2:
    "6월3일부터 6월 9일까지의 삿포로 날씨를 알려줘"
    Output result:
    - Type: Dict
    "location": "sapporo", "country": "jp", "date": "20250603", "year": "2025", "month": "06", "day": "03,04,05,06,07,08,09"
    ############################################################
    USER
    {user_request}
    ############################################################
    """
