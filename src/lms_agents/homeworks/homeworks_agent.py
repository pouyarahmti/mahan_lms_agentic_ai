from typing import List
from agents import function_tool
import requests
from src.config.settings import settings
from src.lms_agents.base_agent import BaseAgent
from src.tools.homeworks.homeworks_tools import (
    get_all_homework_responses,
    get_all_homeworks,
    get_homeworks_by_lesson,
    get_homeworks_responses_by_user,
    get_all_homework_responses_by_homework,
)


class HomeworksAgent(BaseAgent):
    """Agent specialized in handling homeworks-related and homeworks-responses-related queries and operations. You can use this agent to handle homeworks-related and homeworks-responses-related queries and operations."""

    INSTRUCTIONS = """
     You can use this agent to handle homeworks-related queries and operations. You have access to the tools that can be used to handle homeworks-related queries and operations like get_all_homeworks, get_all_homework_responses, get_homework_responses_by_user, get_homeworks_by_lesson, ..... . 
    """

    TOOL_INSTRUCTIONS = """ 
    Tool for handling homeworks-related queries and operations. 
    """

    def __init__(self):
        """Initialize the Homeworks Agent with external tools."""
        tools = [
            get_all_homeworks,
            get_all_homework_responses,
            get_homeworks_by_lesson,
            get_homeworks_responses_by_user,
            get_all_homework_responses_by_homework,
        ]
        super().__init__(
            name="Homeworks Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="homework_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )
