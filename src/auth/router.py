import requests
from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.models import Token
from src.auth.queries import create_token
from src.auth.schemas import GoogleOauth2Request
from src.auth.service import (
    create_access_token,
    create_refresh_token,
    get_or_create_user,
)
from src.auth.utils import verify_refresh_token
from src.config import settings

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
    data = GoogleOauth2Request(code=code, client_id=GOOGLE_CLIENT_ID, client_secret=GOOGLE_CLIENT_SECRET, redirect_uri=GOOGLE_REDIRECT_URI)
    response = requests.post(token_endpoint, data=data.model_dump(mode="json"))
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to obtain token from Google"
        )

    token_json = response.json()
    access_token = token_json["access_token"]
        
    # 2) 토큰으로 사용자 정보 가져오기
    user_info_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_endpoint, headers=headers)
    if user_info_response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch user info from Google"
        )

    user_info = user_info_response.json()

    # 3) 이메일 등을 확인해 내부 DB에 사용자 정보 등록 or 기존 계정 찾기
    user_email = user_info["email"]

    # ... DB 조회/생성 로직 ...
    user = get_or_create_user(user_email)

    # 4) 자체 JWT(또는 세션) 발급하여 로그인 처리
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    token = Token(access_token=access_token, refresh_token=refresh_token)
    token = await create_token(token=token)

    return {
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
        "email": user_email,
    }


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = verify_refresh_token(refresh_token=refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = create_access_token({"sub": payload["sub"]})
    return {"access_token": access_token}
    
    
