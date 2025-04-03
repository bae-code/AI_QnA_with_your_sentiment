from pydantic import BaseModel


class SentimentData(BaseModel):
    result: str
    language: str
    total_evaluation: str
