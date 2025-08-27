from agents import Agent, ModelSettings
from src.config.settings import settings

# AGENTS
from src.lms_agents.courses.course_agent import CourseAgent
from src.lms_agents.lessons.lessons_agent import LessonsAgent
from src.lms_agents.students.students_agent import StudentsAgent
from src.lms_agents.grades.grades_agent import GradesAgent
from agents import Agent, ModelSettings
from src.config.settings import settings
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)
class ManagerAgent:
    """Enhanced manager agent with better orchestration and error handling."""
    
    INSTRUCTIONS = """
    You are an advanced educational assistant for Mahan users with access to specialized agents.
    
    Your role:
    - Coordinate between different specialized agents (Course, Lessons, Students, Grades)
    - Provide comprehensive, well-structured responses
    - Handle complex queries that may require multiple agent interactions
    - Maintain context across multi-step operations
    
    Response Guidelines:
    - Match the user's language (English/Persian)
    - Be friendly, helpful, and encouraging
    - Provide clear explanations and actionable advice
    - When errors occur, explain what went wrong and suggest alternatives
    - Always aim to fully answer the user's question, combining data from multiple sources if needed
    
    Available Agents:
    - Course Agent: Handle course-related queries and operations
    - Lessons Agent: Manage lesson content and structure
    - Students Agent: Access student information and profiles
    - Grades Agent: Retrieve and analyze grade information
    
    For complex requests, break them down into steps and use multiple agents as needed.
    """

    def __init__(self):
        """Initialize the Manager Agent with enhanced coordination."""
        # Initialize specialized agents
        self.course_agent = CourseAgent()
        self.lessons_agent = LessonsAgent()
        self.students_agent = StudentsAgent()
        self.grades_agent = GradesAgent()
        
        # Create main coordinating agent
        self.agent = Agent(
            name="Educational Manager Agent",
            instructions=self.INSTRUCTIONS,
            tools=[
                self.course_agent.agent_tool,
                self.lessons_agent.agent_tool,
                self.students_agent.agent_tool,
                self.grades_agent.agent_tool,
            ],
            model=settings.OPENAI_MODEL,
            model_settings=ModelSettings(
                verbosity="medium", 
                temperature=0.7,
                max_tokens=2000  # Allow for more comprehensive responses
            ),
        )
        
        logger.info("Manager Agent initialized with all specialized agents")
    
    def get_available_capabilities(self) -> Dict[str, List[str]]:
        """Return all capabilities across agents."""
        return {
            "course": self.course_agent.get_capabilities(),
            "lessons": self.lessons_agent.get_capabilities(),
            "students": self.students_agent.get_capabilities(),
            "grades": self.grades_agent.get_capabilities(),
        }
