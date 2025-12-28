from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, Body
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.sys.user import SysUser
from app.schemas.sys.auth import Login, Token, Captcha
from app.utils.captcha import generate_captcha
from app.db.redis import RedisManager
from app.schemas.response import ResponseSchema, response
from app.core.exceptions import APIException
from app.core.codes import ErrorCode


router = APIRouter()


@router.post("/login", response_model=ResponseSchema[Token])
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db), form_data: Login = Body(...)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Check if user is locked due to too many failed attempts
    if await security.is_user_locked(form_data.username):
        raise APIException(
            code=ErrorCode.LOGIN_FAILED,
            message="User account is locked due to too many failed login attempts. Please try again later.",
        )

    result = await db.execute(
        select(SysUser).where(SysUser.username == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        # Increment login attempts
        attempts = await security.get_login_attempts(form_data.username)
        attempts += 1

        # Check if max attempts reached
        if attempts >= settings.MAX_LOGIN_ATTEMPTS:
            # Lock user account
            await security.lock_user_account(form_data.username)
            raise APIException(
                code=ErrorCode.LOGIN_FAILED,
                message="Too many failed login attempts. Account has been locked.",
            )

        # Store updated attempts count
        await security.save_login_attempt(form_data.username, attempts)

        raise APIException(
            code=ErrorCode.LOGIN_FAILED, message="Incorrect username or password"
        )

    if not user.is_active:
        raise APIException(code=ErrorCode.USER_DISABLED, message="Inactive user")

    # Reset login attempts on successful login
    await security.reset_login_attempts(form_data.username)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(user.id, expires_delta=access_token_expires)

    # Save token to Redis
    await security.save_login_token(token, user.id)

    return response(
        data={
            "access_token": token,
            "token_type": "bearer",
        }
    )


@router.get("/captcha", response_model=ResponseSchema[Captcha])
async def get_captcha():
    # Run sync CPU-bound task in threadpool
    b64_str, code = await run_in_threadpool(generate_captcha)

    # Save to redis
    captcha_key = await RedisManager.save_captcha(code)

    return response(
        data=Captcha(
            captcha_base64="data:image/png;base64," + b64_str,
            captcha_key=captcha_key,
        )
    )
