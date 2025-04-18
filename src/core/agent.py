from agents.result import Agent
from agents.result import RunResult
from agents import Runner
from src.core.schema import ResponseQAResult


class BaseAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validate_result(self, result: RunResult):
        return result.final_output_as(self.output_type, raise_if_incorrect_type=True)

    def _get_prompt(self, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")


class ResponseQAAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Response QA Agent",
            instructions="너는 에이전트의 응답이 전달된 프롬프트에 알맞은지 검토해줘. 프롬프트에 명시된 내용이 정확하지 않다고 판단되면 프롬프트에 명시된 형태로 수정해줘. 프롬프트에 명시된 내용이 정확하다고 판단되면 그대로 사용해. 너는 한국어로 대답해야해.",
            output_type=ResponseQAResult,
        )

    async def run(self, prompt: str, response: str) -> dict:
        """Check if the response aligns with the given prompt."""
        check_prompt = self._get_prompt(prompt, response)
        result = await Runner.run(self, input=check_prompt)
        return self._validate_result(result=result)

    def _get_prompt(self, prompt: str, response: str) -> str:
        return f"""
        [프롬프트]
        {prompt}

        [응답]
        {response}

        위의 응답이 프롬프트의 지시사항에 맞게 작성되었는지 확인해주세요.
        - 맞으면: "PASS"를 출력하고 응답 그대로 사용하세요.
        - 틀렸으면: "FAIL"을 출력하고, 프롬프트에 맞게 응답을 수정본과 위반사항을 포함하여 함께 출력해주세요.
        결과는 반드시 다음 JSON 포맷으로 출력하세요:

        {{
            "status": "PASS" | "FAIL",
            "corrected_response": "..."  // PASS인 경우에도 원본 응답 다시 넣어주세요
            "violation": "..."  // 위반사항을 포함하여 함께 출력해주세요.
        }}
        """
