from fastapi import HTTPException, Request, status

from src.auth.utils import verify_access_token, verify_refresh_token


def get_current_user_from_access_token(request: Request):
    access_token = request.headers.get("Authorization")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    payload = verify_access_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return payload


def get_current_user_from_refresh_token(request: Request):
    refresh_token = request.headers.get("Authorization-Refresh")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return payload
