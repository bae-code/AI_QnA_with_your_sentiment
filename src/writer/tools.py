from datetime import datetime


def get_today_context() -> str:
    today = datetime.now()
    return f"Today is {today.strftime('%Y-%m-%d')}"



def korean_spell_check(text: str) -> str:
    return text