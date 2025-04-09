from agents import Runner
from src.core.agent import BaseAgent
from src.writer.schema import WriterData
from src.writer.prompts import letter_writer_prompt
from src.sentiment.schema import SentimentData
from src.writer.tools import get_today_context, get_kr_holiday_data, get_jp_holiday_data


class KoreanLanguageAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Korean Language Agent",
            instructions="너는 한국의 정중하고 따듯한 정서에 맞게 편지를 써야해. 상대의 어투를 분석해서, 상황에 맞게 존댓말을 사용하거나 다정한 친구처럼 대해줘",
            output_type=WriterData,
            tools=[get_kr_holiday_data],
        )


class EnglishLanguageAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="English Language Agent",
            instructions="You write in a casual and friendly tone, as if writing to a friend. Add a bit of warmth and humor when appropriate.",
            output_type=WriterData,
        )


class JapaneseLanguageAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Japanese Language Agent",
            instructions="日本の文化にふさわしい丁寧な文体で、相手に敬意を示しながら心を込めて手紙を書いてください。",
            output_type=WriterData,
            tools=[get_jp_holiday_data],
        )


korean_agent = KoreanLanguageAgent()
english_agent = EnglishLanguageAgent()
japanese_agent = JapaneseLanguageAgent()


class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Letter Writer Agent",
            instructions="You are a letter writer agent. You will be given a text and you will need to write a letter to the user. Passes to the appropriate language agent based on the user's language.",
            output_type=WriterData,
            tools=[get_today_context],
            handoffs=[korean_agent, english_agent, japanese_agent],
        )

    async def write_letter(self, letter: str, sentiment: SentimentData) -> WriterData:
        prompt = self._get_prompt(letter=letter, sentiment=sentiment)
        result = await Runner.run(self, input=prompt)
        return self._validate_result(result=result)

    def _get_prompt(self, letter: str, sentiment: SentimentData) -> str:
        return letter_writer_prompt(
            letter=letter,
            sentiment_data=sentiment.result,
            user_language=sentiment.language,
            total_evaluation=sentiment.total_evaluation,
        )


class PenPalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PenPal Agent",
            instructions="You are a penpal agent. You will be given a text and you will need to write a letter to the user. Use the appropriate language agent tools based on the user's language.",
            output_type=WriterData,
            tools=[
                get_today_context,
                korean_agent.as_tool(
                    tool_name="translate_to_korean",
                    tool_description="Translate the text to Korean",
                ),
                english_agent.as_tool(
                    tool_name="translate_to_english",
                    tool_description="Translate the text to English",
                ),
                japanese_agent.as_tool(
                    tool_name="translate_to_japanese",
                    tool_description="Translate the text to Japanese",
                ),
            ],
        )


pen_pal_agent = PenPalAgent()
writer_agent = WriterAgent()
