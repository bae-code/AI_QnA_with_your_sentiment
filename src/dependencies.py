from fastapi.security import HTTPBearer
from starlette.requests import Request
from fastapi import HTTPException, status
from src.auth.utils import verify_access_token, verify_refresh_token


class AuthRequired(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthRequired, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        access_token = request.headers.get("Authorization")

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized user cannot access",
            )
        token_type, token = access_token.split(" ")

        if token_type != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        try:
            request.state.token_info = verify_access_token(token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )


class RefreshTokenRequired(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(RefreshTokenRequired, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        refresh_token = request.headers.get("Authorization")

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized user cannot access",
            )

        token_type, token = refresh_token.split(" ")

        if token_type != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        try:
            request.state.token_info = verify_refresh_token(token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
