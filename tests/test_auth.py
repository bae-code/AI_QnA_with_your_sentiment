import pytest
import pytest_asyncio
from src.auth.service import get_or_create_user
from src.auth.queries import find_user_by_email
from src.database import mongo_db, mongo_client
from motor.motor_asyncio import AsyncIOMotorCollection


@pytest_asyncio.fixture(loop_scope="session")
def test_user_collection() -> AsyncIOMotorCollection:
    return mongo_db["test_user_collection"]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_or_create_user(test_user_collection):
    user = await get_or_create_user("test@test.com", test_user_collection)
    assert user.email == "test@test.com"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_user_by_email(test_user_collection):
    user = await find_user_by_email("test@test.com", test_user_collection)
    assert user.email == "test@test.com"


@pytest.fixture(scope="session", autouse=True)
def cleanup_after_all_tests():
    yield  # 테스트가 전부 끝날 때까지 기다림
    mongo_client.close()
