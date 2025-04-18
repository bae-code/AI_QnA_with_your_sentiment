import certifi
import ssl
from slack_sdk.web.async_client import AsyncWebClient
from src.config import settings

ssl._create_default_https_context = ssl._create_unverified_context

ssl_context = ssl.create_default_context(cafile=certifi.where())


class SlackClient:
    def __init__(self):
        self.client = AsyncWebClient(token=settings.SLACK_BOT_TOKEN, ssl=ssl_context)
        self.bot_id = "U08P1SQCC9W"

    async def send_message(self, channel: str, message: str):
        members = await self.client.conversations_members(channel=channel)
        if self.bot_id not in members.data["members"]:
            await self.client.conversations_join(channel=channel)
        await self.client.chat_postMessage(channel=channel, text=message)
