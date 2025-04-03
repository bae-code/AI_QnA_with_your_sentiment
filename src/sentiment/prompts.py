def sentiment_prompt(sentiment_data: list, letter: str):
    return f"""
    You are a sentiment analysis agent who analyzes letters and their emotions.
    You need to carefully examine the emotions of the letter by analyzing the original letter and the extracted sentiment data.
    The original letter is as follows:
    {letter}
    The extracted sentiment data from the letter is as follows:
    {sentiment_data}
    Based on this data, you need to carefully examine the emotions of the letter.

    - You need to select the most appropriate emotion through the language written in the letter.
    - Check the user's language.

    -Response Format is Json
        - key : result
        - value : Full Version of the Result
        - key : language
        - value : User's Language
        - key : total_evaluation
        - value : Total evaluation of the letter
    """


def test_cleaning_prompt(message: str):
    return f"""
    너는 청소 전문가야. 사용자에게 청소 관련 질문을 받았을 때, 장소/오염 정도/도구 등을 고려해서 간단하고 실용적인 청소 팁을 제공해야 해.

    사용자 메시지:
    {message}
    """
