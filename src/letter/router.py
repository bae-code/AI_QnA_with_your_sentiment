from fastapi import APIRouter, Body, Depends, HTTPException, status
from starlette.requests import Request

from src.dependencies import AuthRequired
from src.letter.models import LetterContent
from src.letter.schemas import LetterCreateRequest, AiTestLetterRequest
from src.letter.service import LetterService, AiLetterService

router = APIRouter()


@router.post("/send", dependencies=[Depends(AuthRequired())])
async def create_letter(request: Request, body: LetterCreateRequest = Body(...)):
    current_user = request.state.token_info
    letter_service = LetterService()
    letter = LetterContent(
        sender=current_user["sub"],
        receiver=body.receiver,
        content=body.content,
    )
    return await letter_service.create_letter(letter)


@router.get("/{letter_id}", dependencies=[Depends(AuthRequired())])
async def get_letter(letter_id: str, request: Request):
    current_user = request.state.token_info
    letter_service = LetterService()
    letter = await letter_service.get_letter(letter_id)
    if letter:
        letter = await letter_service.read(letter=letter, user_id=current_user["sub"])
    return letter


@router.get("/test/")
async def test_mcp(request: Request):
    from src.forecast.agent import ForecastAgent

    agent = ForecastAgent()
    result = await agent.test_mcp()
    return result


@router.get("/list/", dependencies=[Depends(AuthRequired())])
async def get_letters(request: Request):
    current_user = request.state.token_info
    try:
        letter_service = LetterService()
        letters = await letter_service.get_letters(user_id=current_user["sub"])
        return letters
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/ai")
async def create_ai_letter(body: AiTestLetterRequest = Body(...)):
    letter_service = LetterService()
    ai_letter_service = AiLetterService()
    letter = await letter_service.get_letter(body.letter_id)
    result = await ai_letter_service.execute(letter=letter)
    return result
