from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class Login(BaseModel):
    username: str
    password: str

class Captcha(BaseModel):
    captcha_key: str
    captcha_base64: str