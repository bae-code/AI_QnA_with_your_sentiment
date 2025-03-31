from pydantic import BaseModel


class LetterCreateRequest(BaseModel):
    receiver: str
    content: str
