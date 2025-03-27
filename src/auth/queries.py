from src.auth.models import User


async def find_user_by_email(email: str, collection) -> User | None:
    user = await collection.find_one({"email": email})
    if user:
        return User(**user)
    else:
        return None


async def create_user(user: User, collection) -> User:
    await collection.insert_one(user.model_dump(by_alias=True))
    return user


async def get_user_by_id(user_id: str, collection) -> User | None:
    return await collection.find_one({"_id": user_id})
