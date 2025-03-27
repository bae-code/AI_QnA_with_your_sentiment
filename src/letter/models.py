from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4


class LetterContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    sender: str
    receiver: str
    content: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    read_at: datetime | None = None
    reply_to: str | None = None
