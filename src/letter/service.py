from typing import List
from datetime import datetime

from src.letter.models import LetterContent
from src.letter.queries import LetterQueries

from src.sentiment.agent import SentimentAnalysisAgent, sentiment_agent
from src.writer.agent import WriterAgent, writer_agent
from src.sentiment.schema import SentimentData
from src.writer.schema import WriterData


class LetterService:
    def __init__(self) -> None:
        self.letter_queries = LetterQueries()

    async def create_letter(self, letter: LetterContent):
        await self.letter_queries.create_letter(letter)
        return letter

    async def get_letter(self, letter_id: str) -> LetterContent:
        return await self.letter_queries.get_letter(letter_id)

    async def get_letters(self, user_id: str) -> List[LetterContent]:
        return await self.letter_queries.get_letters(user_id)

    async def read(self, letter: LetterContent, user_id: str):
        if self._is_receiver(user_id=user_id, receiver=letter.receiver):
            data = {"is_read": True, "read_at": datetime.now()}
            await self.letter_queries.update(letter=letter, data=data)
        else:
            pass
        return letter

    def _is_receiver(self, user_id: str, receiver: str) -> bool:
        return receiver == user_id


class AiLetterService(LetterService):
    def __init__(
        self,
        sentiment_agent: SentimentAnalysisAgent = sentiment_agent,
        writer_agent: WriterAgent = writer_agent,
    ) -> None:
        super().__init__()
        self.sentiment_agent = sentiment_agent
        self.writer_agent = writer_agent

    async def write_ai_letter(self, letter: LetterContent) -> WriterData:
        sentiment_result: SentimentData = await self.sentiment_agent.analyze_letter(
            letter=letter.content
        )
        writer_result: WriterData = await self.writer_agent.write_letter(
            letter=letter.content, sentiment=sentiment_result
        )
        print(writer_result)
        return writer_result

    async def execute(self, letter: LetterContent) -> bool:
        ai_reply = await self.write_ai_letter(letter=letter)
        letter = LetterContent(
            sender=letter.receiver,
            receiver=letter.sender,
            content=ai_reply.result,
        )
        await self.create_letter(letter=letter)
        return True
