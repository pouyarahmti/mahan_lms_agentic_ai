from typing import List
from agents import function_tool
import requests
from src.config.settings import settings
from src.lms_agents.base_agent import BaseAgent
from src.tools.students.students_tools import (
    get_all_students,
    get_student_by_id,
)


class StudentsAgent(BaseAgent):
    """Agent specialized in handling students-related queries and operations. You can use this agent to handle students-related queries and operations."""

    INSTRUCTIONS = """
     You can use this agent to handle students-related queries and operations. You have access to the tools that can be used to handle students-related queries and operations like get_all_students, get_student_by_id, ..... . 
    """

    TOOL_INSTRUCTIONS = """ 
    Tool for handling students-related queries and operations. 
    """

    def __init__(self):
        """Initialize the Students Agent with external tools."""
        tools = [
            get_all_students,
            get_student_by_id,
        ]
        super().__init__(
            name="Students Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="students_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )
