"""External Services Agent for handling external services-related queries."""

from typing import List
from lms_agents.base_agent import BaseAgent


class ExternalServicesAgents(BaseAgent):
    """Agent specialized in handling external services queries and operations."""

    instructions = """
    You are an agent specialized in handling external services queries and operations.
    """

    def __init__(self):
        """Initialize the External Agent with external tools."""
        tools = []
        super().__init__(name="External Services Agent", instructions="", tools=tools)
