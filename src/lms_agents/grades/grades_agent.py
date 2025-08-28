from typing import List
from agents import function_tool
import requests
from src.config.settings import settings
from src.lms_agents.base_agent import BaseAgent
from src.tools.grades.grades_tools import (
    get_all_grades,
    get_lesson_grades,
    get_student_grades,
)


class GradesAgent(BaseAgent):
    """Agent specialized in handling grades-related queries and operations. You can use this agent to handle grades-related queries and operations."""

    INSTRUCTIONS = """
     You can use this agent to handle grades-related queries and operations. You have access to the tools that can be used to handle grade-related queries and operations like get_all_grades, get_lesson_grades, get_student_grades, ..... . 
    """

    TOOL_INSTRUCTIONS = """ 
    Tool for handling grades-related queries and operations. 
    """

    def __init__(self):
        """Initialize the Grades Agent with external tools."""
        tools = [
            get_all_grades,
            get_lesson_grades,
            get_student_grades,
        ]
        super().__init__(
            name="Grades Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="grades_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )

    def get_capabilities(self) -> List[str]:
        """Return capabilities of this agent."""
        return [
            "get_all_grades",
            "get_lesson_grades",
            "get_student_grades",
        ]
