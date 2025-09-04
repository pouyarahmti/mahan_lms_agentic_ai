from typing import List
from agents import function_tool
import requests
from src.config.settings import settings
from src.lms_agents.base_agent import BaseAgent
from src.tools.lessons.lessons_tools import (
    get_all_lessons,
    get_lessons_by_course,
)


class LessonsAgent(BaseAgent):
    """Agent specialized in handling lessons-related queries and operations. You can use this agent to handle lessons-related queries and operations."""

    INSTRUCTIONS = """
    You are a Lessons Services Agent specialized in handling lessons-related queries.
    
    Available capabilities:
    - Retrieve all available lessons
    - Filter lessons by course, name, id
    
    Guidelines:
    - Always validate input parameters before making API calls
    - Provide helpful error messages when operations fail
    - Include relevant metadata in your responses (course count, categories, etc.)
    - Be conversational and helpful in your responses
    - If a request fails, suggest alternative approaches
    """

    TOOL_INSTRUCTIONS = """
    Comprehensive tool for lessons-related operations including:
    - Getting all lessons
    - Filtering lessons by id
    - Filtering lessons by course
    - Lesson information retrieval (name, id, description, course, teacher, etc.)
    Use this when users ask about lessons, lesson information, or lesson related queries.
    """

    def __init__(self):
        """Initialize the Lessons Agent with external tools."""
        tools = [
            get_all_lessons,
            get_lessons_by_course,
        ]
        super().__init__(
            name="Lessons Services Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="lessons_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )

    def get_capabilities(self) -> List[str]:
        """Return capabilities of this agent."""
        return [
            "get_all_lessons",
            "get_lessons_by_course",
        ]
