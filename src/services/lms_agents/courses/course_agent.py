from typing import List
from agents import function_tool
import requests
from src.config.settings import settings
from src.services.lms_agents.base_agent import BaseAgent


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
            self.get_all_courses,
            self.get_courses_by_category,
        ]
        super().__init__(
            name="Course Services Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="course_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )

    @function_tool
    def get_all_courses() -> List:
        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        """
        Get a list of all available courses. You can access all the available courses using this tool. In case the user asks for all the available courses.
        """
        try:
            response = requests.get(
                f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/courses/",
                timeout=10,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()["results"]
        except requests.RequestException as e:
            return {"error": str(e)}

    @function_tool
    def get_courses_by_category(category_id: str) -> List:
        """Get a list of all courses for a specific category. You have to pass the category id as a query parameter in the request. Use this tool in case the user asks for courses in a specific category.

        Args:
            category_id (str): The id of the category.
        """

        try:

            headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

            response = requests.get(
                f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/courses/",
                params={"category": category_id},
                timeout=10,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()["results"]
        except requests.RequestException as e:
            return {"error": str(e)}
