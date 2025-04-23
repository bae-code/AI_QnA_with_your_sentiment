import certifi
import ssl
from slack_sdk.web.async_client import AsyncWebClient
from src.config import settings
from enum import Enum

from src.forecast.agent import ForecastAgent, ForecastQueryAgent
from src.forecast.queries import ForecastQueries
from src.core.queries import Q
from src.chat.agent import SlackMessageCoreAgent

ssl._create_default_https_context = ssl._create_unverified_context

ssl_context = ssl.create_default_context(cafile=certifi.where())


class SlackEvent(Enum):
    FILE_SHARED = "file_shared"
    APP_MENTION = "app_mention"

    def __eq__(self, other):
        return self.value == other


class SlackClient:
    def __init__(self):
        self.client = AsyncWebClient(token=settings.SLACK_BOT_TOKEN, ssl=ssl_context)
        self.bot_id = "U08P1SQCC9W"

    async def send_message(self, channel: str, message: str):
        members = await self.client.conversations_members(channel=channel)
        if self.bot_id not in members.data["members"]:
            await self.client.conversations_join(channel=channel)
        await self.client.chat_postMessage(channel=channel, text=message)

    async def run_event(self, event: dict) -> tuple[str, str]:
        self.request_user = event.get("user")
        if event.get("type") == SlackEvent.APP_MENTION:
            user_request = event.get("text").replace(f"<@{self.bot_id}>", "").strip()
            channel = event.get("channel")

            if "날씨" in user_request:
                query_agent = ForecastQueryAgent()
                forecast_agent = ForecastAgent()
                forecast_queries = ForecastQueries()

                query = await query_agent.run(user_request=user_request)

                query = Q.filter(**query.query.model_dump(by_alias=True))

                forecasts = await forecast_queries.get_forecasts(query=query)

                message = await forecast_agent.test_mcp(
                    user_request=user_request, historical_data=forecasts
                )
            else:
                slack_message_core_agent = SlackMessageCoreAgent()
                message = await slack_message_core_agent.run(user_request=user_request)

            await self.send_message(channel=channel, message=message)

            return user_request, channel
