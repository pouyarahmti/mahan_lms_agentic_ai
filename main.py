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
            "Hi there, list me 5 lessons related in the course 013 - مدیرعامل حرفه ای-آنلاین",
        )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
