from typing import List
from src.config.settings import settings
from src.lms_agents.base_agent import BaseAgent
from src.tools.grades.grades_tools import (
    get_all_grades,
    get_lesson_grades,
    get_student_grades,
)


class GradesAgent(BaseAgent):
    """Agent specialized in handling grades-related queries and operations."""

    INSTRUCTIONS = """
    You are a Grades Services Agent specialized in handling grades-related queries.
    
    Available capabilities:
    - Retrieve all available grades
    - Filter grades by lesson
    - Filter grades by student
    
    Guidelines:
    - Always validate input parameters before making API calls
    - Provide helpful error messages when operations fail
    - Include relevant metadata in your responses (grade course, grade lesson, etc.)
    - Be conversational and helpful in your responses
    - If a request fails, suggest alternative approaches
    """

    TOOL_INSTRUCTIONS = """
    Comprehensive tool for grade-related operations including:
    - Getting all grades
    - Filtering grades by lesson
    - Filtering grades by student
    - Grade information retrieval
    Use this when users ask about grades, scores, or academic performance.
    """

    def __init__(self):
        """Initialize the Grades Agent with external tools."""
        tools = [
            get_all_grades,
            get_lesson_grades,
            get_student_grades,
        ]
        super().__init__(
            name="Grades Services Agent", instructions=self.INSTRUCTIONS, tools=tools
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
