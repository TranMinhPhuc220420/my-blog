from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

class UserBase(BaseModel):
    username: str
    hashed_password: str

    device_info: Optional[dict] = None
    refresh_token: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime = None
    updated_at: datetime = None

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
