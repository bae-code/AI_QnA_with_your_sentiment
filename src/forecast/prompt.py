def forecast_prompt(user_request: str) -> str:
    return f"""
    ############################################################
    User Request: {user_request}
    ############################################################
    
    You can only query using one of the following allowed values: 1 or 5.
    If the user provides a number not in this list, use the nearest greater value from the allowed options.
    If the number is greater than 5, use 5 for now — inferred data for higher values will be updated in the future.

    Don't Use ###, #### Markdown Format in Message.
    ############################################################
    
    If the request is for more than 3 days, include a daily forecast list in the message.
    You must use `user_request_days` when it is less than or equal to the actual available forecast days.

    If the user's request exceeds 5 days, only provide up to 5 days of forecast.
    At the end of the message, include the following notice:

    📌 *현재 체험판에서는 최대 5일치까지 예보가 제공됩니다.  
    향후에는 과거 데이터를 기반으로 한 예측 서비스도 제공될 예정입니다.*

    ############################################################
    Message Title:
    :둥근_압핀: [city_name]의 [days]간(start_date ~ end_date)의 날씨 예보입니다!
    ############################################################
    Format Example:
    [emoji_place] *1월1일(월)*
        • 기온: 19°C (66°F)
        • 바람: 남서풍 0~16km/h
        • 예보: 오전 11시까지 이슬비와 안개 가능 :fog: → 이후 맑음 :sunny:

    ############################################################
    Used Emoji List:
    :sunny:
    :rain_cloud:
    :mostly_sunny:
    :fog:
    :cloud:
    :umbrella_with_rain_drops:
    :thunder_cloud_and_rain:
    :partly_sunny_rain:
    :lightning:
    :snowflake:
    ############################################################
    """
