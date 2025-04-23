from fastapi import APIRouter, Body, Depends, HTTPException, status
from starlette.requests import Request

from src.dependencies import AuthRequired
from src.letter.models import LetterContent
from src.letter.schemas import LetterCreateRequest, AiTestLetterRequest
from src.letter.service import LetterService, AiLetterService

from src.forecast.agent import ForecastAgent, ForecastQueryAgent
from src.forecast.queries import ForecastQueries
from src.core.queries import Q

from src.slack.client import SlackClient


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
    user_request = "삿포로 여행을 가려고하는데 6월3일에서 7일까지 날씨좀"
    query_agent = ForecastQueryAgent()
    forecast_agent = ForecastAgent()
    forecast_queries = ForecastQueries()

    query = await query_agent.run(user_request=user_request)

    query = Q.filter(**query.query.model_dump(by_alias=True))

    forecasts = await forecast_queries.get_forecasts(query=query)

    await forecast_agent.test_mcp(user_request=user_request, historical_data=forecasts)
    return True


@router.post("/test/slack")
async def test_slack(request: Request):
    if "X-Slack-Retry-Num" in request.headers:
        return True  # 이미 받은 이벤트임

    slack_client = SlackClient()
    data = await request.json()
    event = data.get("event")
    command = data.get("command")
    user_id = data.get("user_id")
    payload = data.get("payload")
    challenge = data.get("challenge")
    print(event)
    print(command)
    print(user_id)
    print(payload)
    print(challenge)
    if challenge:
        """test용도"""
        return {"challenge": challenge}
    user_request, channel = await slack_client.run_event(event=event)
    return True


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
