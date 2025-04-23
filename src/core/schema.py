from pydantic import BaseModel


class ResponseQAResult(BaseModel):
    status: str
    corrected_response: str
    violation: str
