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
     You can use this agent to handle lessons-related queries and operations. You have access to the tools that can be used to handle course-related queries and operations like get_all_lessons, get_lessons_by_course, get_lessons_by_teacher, ..... . 
    """

    TOOL_INSTRUCTIONS = """ 
    Tool for handling lessons-related queries and operations. 
    """

    def __init__(self):
        """Initialize the Lessons Agent with external tools."""
        tools = [
            get_all_lessons,
            get_lessons_by_course,
        ]
        super().__init__(
            name="Lessons Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="lessons_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )
