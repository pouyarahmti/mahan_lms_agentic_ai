"""External Services Agent for handling external services-related queries."""

from typing import List
from agents.base_agent import BaseAgent


class ExternalServicesAgents(BaseAgent):
    """Agent specialized in handling external services queries and operations."""

    def __init__(self):
        """Initialize the External Agent with external tools."""
        tools = []
        super().__init__(agent_type="external_services", tools=tools)

    def get_capabilities(self) -> List[str]:
        """Return a list of capabilities this agent provides."""
        return [
            "Check student grades and GPA",
            "View pending and completed assignments",
            "Get detailed course information",
            "Submit assignments and projects",
            "Generate academic transcripts",
            "Track academic progress",
            "View semester schedules",
            "Check graduation requirements",
        ]

    def handle_grade_query(self, student_id: str, course_code: str = None) -> str:
        """Handle grade-related queries."""
        query = f"Get grades for student {student_id}"
        if course_code:
            query += f" in course {course_code}"
        return self.run(query)

    def handle_assignment_query(self, student_id: str, course_code: str = None) -> str:
        """Handle assignment-related queries."""
        query = f"Show assignments for student {student_id}"
        if course_code:
            query += f" in course {course_code}"
        return self.run(query)

    def handle_course_query(self, course_code: str) -> str:
        """Handle course information queries."""
        query = f"Get information about course {course_code}"
        return self.run(query)
