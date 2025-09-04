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
    """Agent specialized in handling homeworks-related and homeworks-responses-related queries and operations."""

    INSTRUCTIONS = """
    You are a Homeworks Services Agent specialized in handling homework-related and homework-responses-related queries.
    
    Available capabilities:
    - Retrieve all available homeworks
    - Retrieve all available homework-responses
    - Filter homework-responses by homework
    - Filter homeworks by lesson
    - Filter homework-responses by user
    
    Guidelines:
    - Always validate input parameters before making API calls
    - Provide helpful error messages when operations fail
    - Include relevant metadata in your responses (homeworks count, homework-responses count, etc.)
    - Be conversational and helpful in your responses
    - If a request fails, suggest alternative approaches
    """

    TOOL_INSTRUCTIONS = """
    Comprehensive tool for homework-related operations including:
    - Getting all homeworks
    - Getting all homework-responses
    - Filtering homework-responses by homework
    - Filtering homeworks by lesson
    - Filtering homework-responses by student
    - Homework information retrieval
    - Homework-response information retrieval
    Use this when users ask about homeworks, homework information, or homeworks related content.
    """

    def __init__(self):
        """Initialize the Homeworks Services Agent with external tools."""
        tools = [
            get_all_homeworks,
            get_all_homework_responses,
            get_homeworks_by_lesson,
            get_homeworks_responses_by_user,
            get_all_homework_responses_by_homework,
        ]
        super().__init__(
            name="Homeworks Services Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="homework_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )
