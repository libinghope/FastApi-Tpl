from typing import Optional
import redis.asyncio as redis
from app.core.config import settings

class RedisManager:
    _client: Optional[redis.Redis] = None

    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                encoding="utf-8",
            )
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
            cls._client = None

    @classmethod
    async def set(cls, key: str, value: str, expire: int = None):
        client = cls.get_client()
        await client.set(key, value, ex=expire)

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        client = cls.get_client()
        return await client.get(key)

    @classmethod
    async def delete(cls, key: str):
        client = cls.get_client()
        await client.delete(key)

    @classmethod
    async def save_captcha(cls, code: str, expire: int = 300) -> str:
        """
        save captcha code
        :param code:
        :param expire:
        :return:
        """
        import uuid
        key = str(uuid.uuid4())
        client = cls.get_client()
        await client.set(key, code, ex=expire)
        return key
