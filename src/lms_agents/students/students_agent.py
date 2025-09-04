from typing import List
from agents import function_tool
import requests
from src.config.settings import settings
from src.lms_agents.base_agent import BaseAgent
from src.tools.students.students_tools import (
    get_all_students,
    get_student_by_id,
    get_student_by_name,
)


class StudentsAgent(BaseAgent):
    """Agent specialized in handling students-related queries and operations."""

    INSTRUCTIONS = """
    You are a Student Services Agent specialized in handling student-related queries.
    
    Available capabilities:
    - Retrieve all available students
    - Filter student by name, id
    
    Guidelines:
    - Always validate input parameters before making API calls
    - Provide helpful error messages when operations fail
    - Include relevant metadata in your responses (course count, categories, etc.)
    - Be conversational and helpful in your responses
    - If a request fails, suggest alternative approaches
    """

    TOOL_INSTRUCTIONS = """
    Comprehensive tool for grade-related operations including:
    - Getting all students
    - Filtering grades by id
    - Filtering grades by email
    - Student information retrieval (name, id, email, job, phone number, etc.)
    Use this when users ask about students, student information, or student related queries.
    """

    def __init__(self):
        """Initialize the Students Agent with external tools."""
        tools = [get_all_students, get_student_by_id, get_student_by_name]
        super().__init__(
            name="Students Services Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="students_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )

    def get_capabilities(self) -> List[str]:
        """Return capabilities of this agent."""
        return [
            "get_all_students",
            "get_student_by_id",
            "get_student_by_name",
        ]
