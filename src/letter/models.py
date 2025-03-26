from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4


class LetterContent(BaseModel):
    letter_id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    sender: str
    receiver: str
    content: str
    is_read: bool
    created_at: datetime
    read_at: datetime

class Letters(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    user_id: uuid4
    status: str
    created_at: datetime
    updated_at: datetime
    content_list: list[LetterContent]
    




