from src.auth.models import Token, User
from src.database import token_collection, user_collection


async def find_user_by_email(email: str, collection = user_collection) -> User | None:
    user = await collection.find_one({"email": email})
    if user:
        return User(**user)
    else:
        return None


async def create_user(user: User, collection = user_collection) -> User:
    await collection.insert_one(user.model_dump(by_alias=True))
    return user


async def get_user_by_id(user_id: str, collection = user_collection) -> User | None:
    return await collection.find_one({"_id": user_id})


async def create_token(token: Token, collection = token_collection) -> Token:
    await collection.insert_one(token.model_dump(by_alias=True))
    return token



