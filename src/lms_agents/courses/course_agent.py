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
    """Agent specialized in handling course-related queries and operations."""
    
    INSTRUCTIONS = """
    You are a Course Services Agent specialized in handling course-related queries.
    
    Available capabilities:
    - Retrieve all available courses
    - Filter courses by category
    - Provide course recommendations based on user preferences
    
    Guidelines:
    - Always validate input parameters before making API calls
    - Provide helpful error messages when operations fail
    - Include relevant metadata in your responses (course count, categories, etc.)
    - Be conversational and helpful in your responses
    - If a request fails, suggest alternative approaches
    """
    
    TOOL_INSTRUCTIONS = """
    Comprehensive tool for course-related operations including:
    - Getting all courses
    - Filtering courses by category
    - Course information retrieval
    Use this when users ask about courses, programs, or educational content.
    """

    def __init__(self):
        """Initialize the Course Agent with enhanced tools."""
        tools = [
            get_all_courses,
            get_courses_by_category,
        ]
        
        super().__init__(
            name="Course Services Agent",
            instructions=self.INSTRUCTIONS,
            tools=tools
        )
        
        self.agent_tool = self.agent.as_tool(
            tool_name="course_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )
    
    def get_capabilities(self) -> List[str]:
        """Return capabilities of this agent."""
        return [
            "list_all_courses",
            "filter_courses_by_category",
            "provide_course_information"
        ]
