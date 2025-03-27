from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4


class Chat(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    user_id: str
    title: str = Field(default="")
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_archived: bool = False
    archived_at: datetime | None = None
    is_deleted: bool = False
    deleted_at: datetime | None = None


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    chat_id: str
    pair_id: str
    next_id: str
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
