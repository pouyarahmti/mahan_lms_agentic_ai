from agents import Runner, trace
from src.services.lms_agents.manager.manager_agent import ManagerAgent
import asyncio
import requests
from src.config.settings import settings


async def main():
    manager_agent = ManagerAgent()
    print("TRY TO LIST TOP 5 COURSES AVAILABLE IN MAHAN")
    with trace("User Assistant"):
        result = await Runner.run(
            manager_agent.agent,
            "برای من دوره هایی که توی گروه دوره های سازمانی وجود دارن رو 5 تاشون رو لیست کن",
        )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
