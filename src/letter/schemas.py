from pydantic import BaseModel


class LetterCreateRequest(BaseModel):
    receiver: str
    content: str


class AiTestLetterRequest(BaseModel):
    letter_id: str
