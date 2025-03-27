from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    name: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    is_verified: bool = False
    is_admin: bool = False
    is_superuser: bool = False


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    email: str
