from agents import Runner, trace
from src.core.agent import BaseAgent, ResponseQAAgent
from src.writer.schema import WriterData

from agents.mcp import MCPServerStdio
from src.forecast.prompt import forecast_prompt

from src.slack.choices import Channels
from src.forecast.prompt import rag_forecast_prompt
from src.forecast.schemas import ForecastQuery
from src.writer.tools import get_today_context
from src.forecast.tools import find_fore_cast_with_perplexity


class ForecastAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Forecast Agent",
            instructions=(
                "너는 사용자의 날씨 관련 질문에 응답하는 에이전트야. "
                "모든 응답은 반드시 QA 에이전트를 통해 해석된 질의 결과를 바탕으로 하고, 최종 답변은 반드시 한국어로 출력해야 해. "
                "다음 조건을 정확히 지켜야 해: "
                "1) 사용자가 요청한 날짜에 오늘부터 5일 이내의 날짜가 **하나라도** 포함되어 있다면, 반드시 MCP 툴(get_city_location_info, get_forecast)을 사용해서 응답을 구성해. "
                "2) 요청한 날짜가 전부 오늘로부터 5일 이후라면, MCP 툴을 **절대 사용하지 마.** "
                "3) MCP 또는 예보 데이터가 없는 날짜는 응답에 포함하지 말고, 예보할 수 없다고 안내해. "
                "출력은 보기 좋고 이해하기 쉬운 한국어 예보 문장으로 구성하고, 이모지는 자연스럽게 사용할 수 있지만 필수는 아니야."
            ),
            output_type=WriterData,
            tools=[get_today_context, find_fore_cast_with_perplexity],
        )
        # self.slack_client = SlackClient()
        self.qa_agent = ResponseQAAgent()

    async def test_mcp(
        self, user_request: str, historical_data: list = None
    ) -> WriterData:
        async with MCPServerStdio(
            cache_tools_list=True,
            params={"command": "poetry", "args": ["run", "python", "src/mcp_test.py"]},
        ) as mcp:
            self.mcp_servers = [mcp]
            with trace("mcp_test"):
                self.tools += await mcp.list_tools()

                self.mcp_servers = [mcp]
                qa_feedback = ""
                qa_corrected_response = ""
                for attempt in range(3):
                    print(f"Attempt {attempt + 1} of 3")
                    prompt = (
                        forecast_prompt(
                            user_request=user_request, historical_data=historical_data
                        )
                        + qa_feedback
                        + qa_corrected_response
                    )
                    result = await Runner.run(self, input=prompt)
                    final = self._validate_result(result=result)
                    message = final.result

                    qa_result = await self.qa_agent.run(prompt=prompt, response=message)
                    if qa_result.status == "PASS":
                        message = qa_result.corrected_response
                        break
                    else:
                        qa_corrected_response = qa_result.corrected_response
                        qa_result = await self.qa_agent.run(
                            prompt=prompt + qa_result.violation,
                            response=qa_corrected_response,
                        )
                        if qa_result.status == "PASS":
                            message = qa_result.corrected_response
                            print(f"QA Count: {attempt + 1}")
                            break
                        else:
                            qa_feedback = f"위반사항: {qa_result.violation}"
                            print(qa_feedback)
                return message
                await self.slack_client.send_message(
                    channel=Channels.random_channel, message=message
                )

                return final


class ForecastQueryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Forecast Query Agent",
            instructions="You make a query to search the forecast data in the database.",
            output_type=ForecastQuery,
            tools=[get_today_context],
        )

    def _get_prompt(self, user_request: str):
        return rag_forecast_prompt(user_request=user_request)

    async def run(self, user_request: str) -> ForecastQuery:
        prompt = self._get_prompt(user_request=user_request)

        result = await Runner.run(self, input=prompt)

        return self._validate_result(result=result)
