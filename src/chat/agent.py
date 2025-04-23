from src.core.agent import BaseAgent
from agents.run import Runner


class SlackMessageCoreAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Slack Message Core Agent",
            instructions=(
                "너는 사용자의 메시지를 해석하고, 적절한 응답을 반환하는 에이전트야."
                "아주 친구같고 건방진 말투를 써도 좋아."
                "슬랙메세지 형식에 맞게 응답해야해"
                "반드시 한국어를써야해"
                "어이없는 시비걸면  꼭'디질래' 라고 말해"
                "굉장히 어이없으면 ? 하나만 작성해"
            ),
            output_type=str,
        )

    def _get_prompt(self, user_request: str):
        return f"사용자의 메시지: {user_request}"

    async def run(self, user_request: str):
        prompt = self._get_prompt(user_request=user_request)
        result = await Runner.run(self, input=prompt)
        final = self._validate_result(result)
        return final
