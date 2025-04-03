from agents import Agent, Runner

from sentiment.client import hugging_face_client
from sentiment.prompts import sentiment_prompt
from sentiment.schema import SentimentData


class SentimentAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Sentiment Analysis Agent",
            instructions="You are a sentiment analysis agent. You will be given a text and you will need to analyze the sentiment of the text.",
            output_type=SentimentData,
        )
        self.analysis_client = hugging_face_client

    def analyze_data(self, text: str):
        return self.analysis_client.classify(text)

    def analyze_with_openai(self, prompt: str):
        Runner.run(self, input=prompt)

    async def analyze_letter(self, letter: str):
        extracted_data = self._extract_window_sliding(letter)
        sentiment_results = [self.analyze_data(i) for i in extracted_data]
        prompt = sentiment_prompt(sentiment_results, letter)
        result = await Runner.run(self, input=prompt)
        return result

    def _extract_window_sliding(self, letter: str):
        # TODO : Refactor sliding window
        letter_sliding_windows = []
        letter_splits = [i for i in letter.split("\n") if len(i) > 1]
        for i, _ in enumerate(letter_splits):
            window = letter_splits[i : i + 2]

            letter_sliding_windows.append(window)

        return letter_sliding_windows
