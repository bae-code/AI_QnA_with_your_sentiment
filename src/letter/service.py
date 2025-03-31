from typing import List
from datetime import datetime

from src.letter.models import LetterContent
from src.letter.queries import LetterQueries


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

    async def read(self, letter: LetterContent):
        data = {"is_read": True, "read_at": datetime.now()}
        await self.letter_queries.update(letter=letter, data=data)
        return letter
