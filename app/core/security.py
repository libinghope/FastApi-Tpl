from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # bcrypt限制密码长度为72字节
    password = password[:72]
    return pwd_context.hash(password)


from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import jwt
from app.core.config import settings
from app.db.redis import RedisManager

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def save_login_token(token: str, user_id: int) -> None:
    """
    Save login token to Redis with expiration
    """
    await RedisManager.set(
        f"login_token:{token}",
        str(user_id),
        expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


async def validate_login_token(token: str) -> Optional[str]:
    """
    Validate login token exists in Redis
    """
    return await RedisManager.get(f"login_token:{token}")


async def delete_login_token(token: str) -> None:
    """
    Delete login token from Redis
    """
    await RedisManager.delete(f"login_token:{token}")


async def save_login_attempt(username: str, attempts: int) -> None:
    """
    Save login attempts to Redis with expiration
    """
    await RedisManager.set(
        f"login_attempts:{username}",
        str(attempts),
        expire=settings.LOGIN_LOCKOUT_MINUTES * 60,
    )


async def get_login_attempts(username: str) -> int:
    """
    Get login attempts from Redis
    """
    attempts_str = await RedisManager.get(f"login_attempts:{username}")
    return int(attempts_str) if attempts_str else 0


async def lock_user_account(username: str) -> None:
    """
    Lock user account in Redis with expiration
    """
    await RedisManager.set(
        f"login_lockout:{username}", "1", expire=settings.LOGIN_LOCKOUT_MINUTES * 60
    )


async def is_user_locked(username: str) -> bool:
    """
    Check if user account is locked in Redis
    """
    return await RedisManager.get(f"login_lockout:{username}") is not None


async def reset_login_attempts(username: str) -> None:
    """
    Reset login attempts and lockout status for user
    """
    await RedisManager.delete(f"login_attempts:{username}")
    await RedisManager.delete(f"login_lockout:{username}")
