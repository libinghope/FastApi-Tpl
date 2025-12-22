from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str
    nickname: Optional[str] = None
    gender: int = 1
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    is_active: bool = True
    dept_id: Optional[int] = None
    remark: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    id: int
    nickname: Optional[str] = None
    gender: Optional[int] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None
    dept_id: Optional[int] = None
    remark: Optional[str] = None
    # Add other fields as necessary

class UserResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    is_superuser: bool
    # Computed/related fields
    role_ids: List[int] = []
    
    class Config:
        from_attributes = True

class UserEditForm(BaseModel):
    id: Optional[int] = None # If None, it's an add, else update
    username: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[int] = 1
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True
    dept_id: Optional[int] = None
    role_ids: List[int] = []

class ChangeStatusForm(BaseModel):
    user_uid: int
    status: bool

class ModifyPasswordForm(BaseModel):
    id: int
    password: str
    password2: str

class DeleteObjsForm(BaseModel):
    uid_arr: List[int]

class BindPhoneForm(BaseModel):
    user_uid: int
    phone: str
    code: str

class BindEmailForm(BaseModel):
    user_uid: int
    email: str
    code: str

class UserProfileForm(BaseModel):
    nickname: Optional[str] = None
    gender: Optional[int] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
