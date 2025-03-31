from src.core.queries import BaseQueries, Q
from src.database import letter_collection
from src.letter.models import LetterContent
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List
from datetime import datetime


class LetterQueries(BaseQueries):
    def __init__(self, collection: AsyncIOMotorCollection = letter_collection) -> None:
        super().__init__(collection)

    async def create_letter(self, letter: LetterContent) -> LetterContent:
        return await self.collection.insert_one(letter.model_dump(by_alias=True))

    async def get_letter(self, letter_id: str) -> LetterContent:
        letter = await self.find_one(_id=letter_id)
        return LetterContent(**letter)

    async def get_letters(self, user_id: str) -> List[LetterContent]:
        return await self.find(query=Q.or_(sender=user_id, receiver=user_id))

    async def update(self, letter: LetterContent, data: dict) -> LetterContent:
        return await self.find_and_update(data=data, query=Q({"_id": letter.id}))
