from agents.result import Agent
from pydantic import BaseModel
from agents.result import RunResult


class BaseAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validate_result(self, result: RunResult):
        return result.final_output_as(self.output_type, raise_if_incorrect_type=True)

    def _get_prompt(self, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")
