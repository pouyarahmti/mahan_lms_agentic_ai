from agents import Runner, trace
from openai.types.responses import ResponseTextDeltaEvent

from src.lms_agents.manager.manager_agent import ManagerAgent
import asyncio
import requests
from src.config.settings import settings


async def main():
    manager_agent = ManagerAgent()
    with trace("User Assistant"):
        result = Runner.run_streamed(
            manager_agent,
            input="List me the homework responses of the student  'نوبخت علیپور'  and take the average of the scores.",
        )
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
