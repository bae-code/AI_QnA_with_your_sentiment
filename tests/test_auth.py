import pytest
import pytest_asyncio
from src.auth.service import AuthService
from src.auth.utils import verify_access_token, check_expired_token
from src.database import mongo_db, mongo_client
from motor.motor_asyncio import AsyncIOMotorCollection


@pytest_asyncio.fixture(loop_scope="session")
def test_user_collection() -> AsyncIOMotorCollection:
    return mongo_db["test_user_collection"]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_or_create_user(test_user_collection):
    auth_service = AuthService()
    user = await auth_service.get_or_create_user("test@test.com")
    assert user.email == "test@test.com"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_user_by_email(test_user_collection):
    auth_service = AuthService()
    user = await auth_service.user_queries.find_user_by_email("test@test.com")
    assert user.email == "test@test.com"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_access_token(test_user_collection):
    auth_service = AuthService()
    token = auth_service.create_access_token({"sub": "test@test.com"})
    assert token is not None
    verified_token = verify_access_token(token)
    assert verified_token is not None
    assert verified_token == True


@pytest.fixture(scope="session", autouse=True)
def cleanup_after_all_tests():
    yield  # 테스트가 전부 끝날 때까지 기다림
    print("\n🧹 테스트 세션 종료: Mongo 클라이언트 종료 중...")
    mongo_client.close()
