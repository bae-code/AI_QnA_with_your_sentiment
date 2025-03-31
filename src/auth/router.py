import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.auth.dependencies import (
    get_current_user_from_access_token,
    get_current_user_from_refresh_token,
)
from src.auth.models import Token
from src.auth.queries import TokenQueries
from src.auth.schemas import GoogleOauth2Request
from src.auth.service import AuthService
from src.config import settings
from src.dependencies import AuthRequired, RefreshTokenRequired

router = APIRouter()

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI


@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&response_type=code&scope=email profile"
    }


@router.get("/google/callback", status_code=status.HTTP_200_OK)
async def auth_google_callback(code: str):
    token_endpoint = "https://oauth2.googleapis.com/token"
    data = GoogleOauth2Request(
        code=code,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )
    response = requests.post(token_endpoint, data=data.model_dump(mode="json"))
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to obtain token from Google",
        )

    token_json = response.json()
    access_token = token_json["access_token"]

    # 2) 토큰으로 사용자 정보 가져오기
    user_info_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_endpoint, headers=headers)
    if user_info_response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch user info from Google",
        )

    user_info = user_info_response.json()

    # 3) 이메일 등을 확인해 내부 DB에 사용자 정보 등록 or 기존 계정 찾기
    user_email = user_info["email"]

    # ... DB 조회/생성 로직 ...
    auth_service = AuthService()
    user = await auth_service.get_or_create_user(user_email)

    # 4) 자체 JWT(또는 세션) 발급하여 로그인 처리
    access_token = auth_service.create_access_token({"sub": user.id})
    refresh_token = auth_service.create_refresh_token({"sub": user.id})
    token = Token(access_token=access_token, refresh_token=refresh_token)
    token_queries = TokenQueries()
    token = await token_queries.create_token(token=token)

    return {
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
        "email": user_email,
    }


@router.post("/refresh", dependencies=[Depends(RefreshTokenRequired())])
async def issue_access_token(request: Request):
    current_user = request.state.token_info
    auth_service = AuthService()
    token_queries = TokenQueries()
    access_token = auth_service.create_access_token({"sub": current_user["sub"]})
    token = await token_queries.access_token_refresh(
        access_token=access_token, refresh_token=request.state.refresh_token
    )
    if token:
        return {
            "access_token": token.access_token,
            "refresh_token": token.refresh_token,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


@router.post("/me")
async def me(current_user: dict = Depends(get_current_user_from_access_token)):
    return current_user
