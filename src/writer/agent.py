from agents import Agent, Runner
from writer.schema import WriterData


class WriterAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Letter Writer Agent",
            instructions="You are a letter writer agent. You will be given a text and you will need to write a letter to the user.",
            output_type=WriterData,
        )

    async def write_letter(self, prompt: str):
        result = await Runner.run(self, input=prompt)
        return result
