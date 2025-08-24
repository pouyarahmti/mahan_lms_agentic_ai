from agents import Runner, trace
from src.lms_agents.manager.manager_agent import ManagerAgent
import asyncio
import requests
from src.config.settings import settings


async def main():
    manager_agent = ManagerAgent()
    with trace("User Assistant"):
        result = await Runner.run(
            manager_agent.agent,
            "List me the details of an student with the name of روح اله باطنی",
        )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
