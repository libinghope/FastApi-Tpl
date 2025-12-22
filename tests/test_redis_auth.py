import asyncio
import sys
import os
from datetime import timedelta

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.core import security
from app.core.config import settings
from app.db.redis import RedisManager
from app.api.deps import get_current_user
from fastapi import HTTPException

# Mock objects
class MockUser:
    id = 1
    username = "testuser"
    is_active = True
    hashed_password = "hash"

class MockDB:
    async def execute(self, stmt):
        class Result:
            def scalar_one_or_none(self):
                return MockUser()
        return Result()

async def main():
    print("Testing Redis Auth Flow...")
    
    # 1. Simulate Login (Store Token)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    user_id = 1
    token = security.create_access_token(
        user_id, expires_delta=access_token_expires
    )
    
    print(f"Generated Token: {token}")
    
    # Store in Redis
    await RedisManager.set(
        f"login_token:{token}", 
        str(user_id), 
        expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    print("Stored token in Redis.")

    # 2. Verify Redis Check (Success case)
    stored_uid = await RedisManager.get(f"login_token:{token}")
    assert stored_uid == str(user_id), f"Redis GET failed. Expected {user_id}, got {stored_uid}"
    print("Redis verification successful.")

    # 3. Simulate get_current_user (Dependency check)
    # We can't easily invoke the Dependency directly with FastAPI dependency injection machinery here,
    # but we can call the function with mocked args.
    
    try:
        user = await get_current_user(db=MockDB(), token=token)
        print(f"get_current_user returned: {user.username}")
    except Exception as e:
        print(f"get_current_user failed: {e}")
        raise e

    # 4. Verify Logout/Invalid Token (Failure case)
    await RedisManager.delete(f"login_token:{token}")
    print("Deleted token from Redis (Logout).")
    
    try:
        await get_current_user(db=MockDB(), token=token)
        print("Error: get_current_user should have failed!")
    except HTTPException as e:
        print(f"Caught expected exception: {e.detail}")
        if e.status_code == 401:
            print("Status code 401 confirmed.")
    
    await RedisManager.close()

if __name__ == "__main__":
    asyncio.run(main())
