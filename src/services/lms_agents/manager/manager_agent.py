from typing import List
from agents import function_tool, Agent, ModelSettings
import requests
from src.config.settings import settings
from src.services.lms_agents.courses.course_agent import CourseAgent


class ManagerAgent:

    INSTRUCTIONS = """You are an educational assistant for Mahan users. You have access to various tools that can be used to answer to the user as complete as possible. \
        You can combine the results of the tools to create a complete answer to the user's question. \
        You have access to the tools that can be used to handle course-related queries and operations like get_all_courses, get_course_info, get_courses_by_category, ..... . \
        You can either respond back to the user in English or in Persian. Mainly respond in Persian. \
        Always provide clear, helpful responses about academic matters. \
        Also don't be too cold or too formal. Be friendly and helpful. Be honest and help the user to improve their academic performance. """

    def __init__(self):
        """Initialize the Manager Agent with all available tools."""
        self.agent = Agent(
            name="Manager Agent",
            instructions=self.INSTRUCTIONS,
            tools=[CourseAgent().agent_tool],
            model=settings.OPENAI_MODEL,
            model_settings=ModelSettings(verbosity="medium", temperature=0.7),
        )
