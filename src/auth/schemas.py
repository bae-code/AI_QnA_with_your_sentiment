from pydantic import BaseModel

class GoogleOauth2Request(BaseModel):
    code: str
    client_id: str
    client_secret: str
    redirect_uri: str
    grant_type: str = "authorization_code"