from agents import Runner
from core.agent import BaseAgent
from writer.schema import WriterData
from writer.prompts import letter_writer_prompt
from sentiment.schema import SentimentData
from writer.tools import get_today_context


class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Letter Writer Agent",
            instructions="You are a letter writer agent. You will be given a text and you will need to write a letter to the user.",
            output_type=WriterData,
            tools=[get_today_context],
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


class KoreanLanguageWriterAgent(WriterAgent):
    def __init__(self):
        super().__init__()
        self.name = "Korean Language Writer Agent"
        self.instructions = "You are a letter writer agent. You will be given a text and you will need to write a letter to the user."
        self.output_type = WriterData


class EnglishLanguageWriterAgent(WriterAgent):
    def __init__(self):
        super().__init__()
        self.name = "English Language Writer Agent"
        self.instructions = "You are a letter writer agent. You will be given a text and you will need to write a letter to the user."
        self.output_type = WriterData


class JapaneseLanguageWriterAgent(WriterAgent):
    def __init__(self):
        super().__init__()
        self.name = "Japanese Language Writer Agent"
        self.instructions = "You are a letter writer agent. You will be given a text and you will need to write a letter to the user."
        self.output_type = WriterData
