from motor.motor_asyncio import AsyncIOMotorCollection

from src.auth.models import Token, User
from src.core.queries import BaseQueries
from src.database import token_collection, user_collection


class UserQueries(BaseQueries):
    def __init__(self, collection: AsyncIOMotorCollection = user_collection) -> None:
        super().__init__(collection)

    async def find_user_by_email(self, email: str) -> User | None:
        user = await self.find_one(email=email)
        if user:
            return User(**user)
        else:
            return None

    async def create_user(self, user: User) -> User:
        await self.create(data=user.model_dump(by_alias=True))
        return user

    async def get_user_by_id(self, user_id: str) -> User | None:
        return await self.find_one(_id=user_id)


class TokenQueries(BaseQueries):
    def __init__(self, collection: AsyncIOMotorCollection = token_collection) -> None:
        super().__init__(collection)

    async def create_token(self, token: Token) -> Token:
        await self.create(data=token.model_dump(by_alias=True))
        return token
