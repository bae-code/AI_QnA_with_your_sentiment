from src.auth.models import User
from src.auth.queries import find_user_by_email, create_user


async def get_or_create_user(email: str, collection) -> User:
    user = await find_user_by_email(email=email, collection=collection)
    if user:
        return user
    else:
        user = User(email=email, name="")
        await create_user(user=user, collection=collection)
        return user
