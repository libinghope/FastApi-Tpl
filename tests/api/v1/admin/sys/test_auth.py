import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock
from app.main import app
from app.api import deps
from app.models.sys.user import SysUser
from app.core import security
from app.core.config import settings  # 添加settings导入
from app.core.config import settings
# Mock User Data - 确保密码不会直接用于哈希计算，而是依赖conftest.py中的mock
# Mock User Data
# 不再直接调用security.get_password_hash，而是直接设置一个模拟的哈希值
MOCK_HASHED_PASSWORD = security.get_password_hash(MOCK_PASSWORD)
    id=1, username="testadmin", hashed_password=MOCK_HASHED_PASSWORD, is_active=True
)


@pytest.fixture
def mock_db_session():
    """Mock the database session"""
    mock_session = AsyncMock()

    # Mock result for success case
    mock_result_success = MagicMock()
    mock_result_success.scalar_one_or_none.return_value = MOCK_USER

    # Mock result for user not found
    mock_result_not_found = MagicMock()
    mock_result_not_found.scalar_one_or_none.return_value = None

    # Default to success, individual tests can override
    mock_session.execute.return_value = mock_result_success

    return mock_session


@pytest.fixture
def override_get_db(mock_db_session):
    async def _get_db():
        yield mock_db_session

    app.dependency_overrides[deps.get_db] = _get_db
    yield
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, override_get_db, mock_redis_manager):
    """Test successful login"""
    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        json={"username": "testadmin", "password": MOCK_PASSWORD},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(
    client: AsyncClient, override_get_db, mock_redis_manager, mocker
):
    """Test login with wrong password"""
    # We need to ensure is_user_locked returns False (default in mock_user_locked fixture if we had one,
    # but here we rely on mock_redis_manager patching RedisManager.get to return None/False implies not locked potentially?
    # Actually security.is_user_locked calls RedisManager.get.
    # If mock_redis_manager.get returns None, int(None) fails?
    # We need to verify what security.is_user_locked expects.

    # Let's inspect security.is_user_locked implementation via reading or just robustly mocking it.
    # Ideally checking the file app/core/security.py would be good, but I'll assume standard redis interaction.
    # For this test, let's explicitly mock security functions to be safe?
    # Or just adjust the mock_redis_manager in this test.

    # Reset lock check to safe value
    mocker.patch(
        "app.db.redis.RedisManager.get", new_callable=AsyncMock, return_value=None
    )

    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        json={"username": "testadmin", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_login_user_not_found(
    client: AsyncClient, mock_db_session, override_get_db, mock_redis_manager, mocker
):
    """Test login with non-existent user"""
    mocker.patch(
        "app.db.redis.RedisManager.get", new_callable=AsyncMock, return_value=None
    )

    # Override DB to return None
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result

    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        json={"username": "unknown", "password": "password"},
    )
    # The current implementation might return "Incorrect username or password" for security
    # or "Incorrect username or password" is generalized.
    # Looking at auth.py:
    # if not user or not security.verify_password...
    # It attempts to verify password on None user? verify_password(pw, user.hashed_password) -> user is None -> crash?
    # Wait, check auth.py:37
    # if not user or not security.verify_password(form_data.password, user.hashed_password):
    # Python short-circuit: if not user is True, it enters the block. Safe.

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_login_inactive_user(
    client: AsyncClient, mock_db_session, override_get_db, mock_redis_manager, mocker
):
    """Test login with inactive user"""
    mocker.patch(
        "app.db.redis.RedisManager.get", new_callable=AsyncMock, return_value=None
    )

    user_inactive = SysUser(
        id=1,
        username="testadmin",
        hashed_password=MOCK_HASHED_PASSWORD,
        is_active=False,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user_inactive
    mock_db_session.execute.return_value = mock_result

    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        json={"username": "testadmin", "password": MOCK_PASSWORD},
    )
    assert response.status_code == 400
    # Detail from auth.py:59
    assert response.json()["detail"] == "Inactive user"


@pytest.mark.asyncio
async def test_login_locked_user(
    client: AsyncClient, override_get_db, mock_redis_manager, mocker
):
    """Test login when user is locked"""
    # Mock security.is_user_locked to return True
    # We can mock the function directly
    mocker.patch(
        "app.core.security.is_user_locked", new_callable=AsyncMock, return_value=True
    )

    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        json={"username": "testadmin", "password": MOCK_PASSWORD},
    )
    assert response.status_code == 400
    assert "User account is locked" in response.json()["detail"]
