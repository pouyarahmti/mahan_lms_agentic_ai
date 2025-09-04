from agents import Runner, trace
from openai.types.responses import ResponseTextDeltaEvent

from src.lms_agents.manager.manager_agent import ManagerAgent
import asyncio
import requests
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)


async def main():
    """Enhanced main function with comprehensive error handling."""
    try:
        manager_agent = ManagerAgent()

        # Log available capabilities
        capabilities = manager_agent.get_available_capabilities()
        logger.info(f"System ready with capabilities: {capabilities}")

        with trace("User Assistant Session"):
            result = await Runner.run(
                manager_agent.agent,
                "hi. please list me top 5 courses in Mahan.",
                max_turns=100,
            )

            if result.final_output:
                print("✅ Response:")
                print(result.final_output)
            else:
                print("❌ No response generated")

    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Application failed: {e}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    asyncio.run(main())
