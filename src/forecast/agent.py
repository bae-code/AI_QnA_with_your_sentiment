from agents import Runner, trace
from src.core.agent import BaseAgent, ResponseQAAgent
from src.writer.schema import WriterData

from agents.mcp import MCPServerStdio
from src.forecast.prompt import forecast_prompt
from src.slack.client import SlackClient
from src.slack.choices import Channels


class ForecastAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Forecast Agent",
            instructions="반드시 MCP 툴(get_city_location_info,get_forecast)을 사용해서 대답해. 반드시 한국어로 대답해야해, QA 에이전트를 반드시 거쳐야해",
            output_type=WriterData,
        )
        self.slack_client = SlackClient()
        self.qa_agent = ResponseQAAgent()

    async def test_mcp(self) -> WriterData:
        async with MCPServerStdio(
            cache_tools_list=True,
            params={"command": "poetry", "args": ["run", "python", "src/mcp_test.py"]},
        ) as mcp:
            self.mcp_servers = [mcp]
            with trace("mcp_test"):
                tools = await mcp.list_tools()
                self.mcp_servers = [mcp]
                qa_feedback = ""
                for attempt in range(3):
                    print(f"Attempt {attempt + 1} of 3")
                    prompt = (
                        forecast_prompt(user_request="삿포로 일주일간 날씨는 어때?")
                        + qa_feedback
                    )
                    result = await Runner.run(self, input=prompt)
                    final = self._validate_result(result=result)
                    message = final.result

                    qa_result = await self.qa_agent.run(prompt=prompt, response=message)
                    if qa_result.status == "PASS":
                        message = qa_result.corrected_response
                        break
                    else:
                        qa_feedback = f"위반사항: {qa_result.violation}"
                await self.slack_client.send_message(
                    channel=Channels.random_channel, message=message
                )

                return final
