from agents import Runner

from sentiment.client import hugging_face_client
from sentiment.prompts import sentiment_prompt
from sentiment.schema import SentimentData
from core.agent import BaseAgent


class SentimentAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Sentiment Analysis Agent",
            instructions="You are a sentiment analysis agent. You will be given a text and you will need to analyze the sentiment of the text.",
            output_type=SentimentData,
        )
        self.analysis_client = hugging_face_client

    def analyze_data(self, text: str) -> list:
        return self.analysis_client.classify(text)

    async def analyze_letter(self, letter: str) -> SentimentData:
        extracted_data = self._extract_window_sliding(letter)
        sentiment_results = [self.analyze_data(i) for i in extracted_data]
        prompt = self._get_prompt(sentiment_data=sentiment_results, letter=letter)
        result = await Runner.run(self, input=prompt)
        return self._validate_result(result=result)

    def _extract_window_sliding(self, letter: str) -> list:
        # TODO : Refactor sliding window
        letter_sliding_windows = []
        letter_splits = [i for i in letter.split("\n") if len(i) > 1]
        for i, _ in enumerate(letter_splits):
            window = letter_splits[i : i + 2]

            letter_sliding_windows.append(window)

        return letter_sliding_windows

    def _get_prompt(self, sentiment_data: list, letter: str) -> str:
        return sentiment_prompt(sentiment_data=sentiment_data, letter=letter)
