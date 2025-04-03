from pydantic import BaseModel


class WriterData(BaseModel):
    result: str
    language: str
