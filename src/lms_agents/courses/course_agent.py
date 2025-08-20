from typing import List
from agents import function_tool
import requests
from src.config.settings import settings
from src.lms_agents.base_agent import BaseAgent
from src.tools.course.course_tools import (
    get_all_courses,
    get_courses_by_category,
)


class CourseAgent(BaseAgent):
    """Agent specialized in handling course-related queries and operations. You can use this agent to handle course-related queries and operations."""

    INSTRUCTIONS = """
    You are an agent specialized in handling external services queries and operations. You can use this agent to handle course-related queries and operations. You have access to the tools that can be used to handle course-related queries and operations like get_all_courses, get_course_info, get_courses_by_category, ..... . 
    """

    TOOL_INSTRUCTIONS = """ 
    Tool for handling course-related queries and operations. 
    """

    def __init__(self):
        """Initialize the Course Agent with external tools."""
        tools = [
            get_all_courses,
            get_courses_by_category,
        ]
        super().__init__(
            name="Course Services Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="course_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )
