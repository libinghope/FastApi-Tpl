
import sys
from unittest.mock import MagicMock

# Mock PIL if not present to avoid ImportError in tests
try:
    import PIL
except ImportError:
    sys.modules["PIL"] = MagicMock()
    sys.modules["PIL.Image"] = MagicMock()
    sys.modules["PIL.ImageDraw"] = MagicMock()
    sys.modules["PIL.ImageFont"] = MagicMock()

import asyncio
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app

from app.core import security
from app.core.config import settings
from app.api import deps

# Use an in-memory SQLite database for testing, or a separate test database
# For this example, we'll assume we can use the same DB or a test DB config.
# Ideally, use a separate test DB.
# settings.SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"

# Mock Redis
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture(scope="function")
async def client() -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

@pytest.fixture(scope="module")
def mock_redis():
    """Mock Redis functionality"""
    mock = MagicMock()
    
    # Mock specific methods used in auth.py
    # create_access_token calls save_login_token which calls RedisManager.set
    # is_user_locked calls RedisManager.get
    # get_login_attempts calls RedisManager.get
    # save_login_attempt calls RedisManager.set
    # reset_login_attempts calls RedisManager.delete
    
    # We need to patch the methods in app.core.security where they are likely used or 
    # patch app.db.redis.RedisManager directly if that's what's used.
    # Looking at auth.py: 
    # await security.is_user_locked(form_data.username)
    # await security.save_login_token(token, user.id)
    # await security.get_login_attempts(form_data.username)
    # await security.save_login_attempt(form_data.username, attempts) 
    # await security.reset_login_attempts(form_data.username)

    # Let's mock the security module functions directly for simplicity in this unit test scope,
    # OR we can mock the underlying Redis calls if we want to test the security module logic too.
    # Given the request is "add test cases for login", integrating the security logic is better.
    # So let's mock app.db.redis.RedisManager.
    
    pass

@pytest.fixture(autouse=True)
def mock_redis_manager(mocker):
    # Mock the RedisManager class methods
    mocker.patch("app.db.redis.RedisManager.get", new_callable=AsyncMock, return_value=None)
    mocker.patch("app.db.redis.RedisManager.set", new_callable=AsyncMock)
    mocker.patch("app.db.redis.RedisManager.delete", new_callable=AsyncMock)

@pytest.fixture(autouse=True)
def mock_password_hashing(mocker):
    # 模拟密码哈希函数，避免bcrypt长度限制问题
    mocker.patch("app.core.security.get_password_hash", return_value="hashed_password")
    mocker.patch("app.core.security.verify_password", return_value=True)

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"
