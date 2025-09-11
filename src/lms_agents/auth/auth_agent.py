from typing import List
from src.lms_agents.base_agent import BaseAgent
from src.tools.auth.auth_tools import (
    authenticate_user,
)


class AuthenticationAgent(BaseAgent):
    """Agent specialized in user authentication and identity verification."""

    INSTRUCTIONS = """
    You are an Authentication Agent specialized in verifying users and students.
    
    Available capabilities:
    - Authenticate users by credentials
    
    Guidelines:
    - Handle sensitive data carefully
    - Provide clear success/failure messages
    - Suggest corrective actions for failed authentication
    - Be professional and secure
    """

    TOOL_INSTRUCTIONS = """
    Tools for authentication:
    - User authentication by credentials
    - Manage authentication sessions
    Use this when users ask about login, identity verification, or secure access.
    """

    def __init__(self):
        tools = [
            authenticate_user,
        ]

        super().__init__(
            name="Authentication Agent", instructions=self.INSTRUCTIONS, tools=tools
        )

        self.agent_tool = self.agent.as_tool(
            tool_name="authentication_tool",
            tool_description=self.TOOL_INSTRUCTIONS,
        )

    def get_capabilities(self) -> List[str]:
        return [
            "authenticate_user",
        ]
