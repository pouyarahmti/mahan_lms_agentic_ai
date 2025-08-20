"""Base agent class for the Student Assistant System."""

from abc import ABC, abstractmethod
from typing import List, Any
from smolagents import LiteLLMModel, CodeAgent
from src.config.settings import settings
from agents import Agent


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(
        self,
        name: str,
        instructions: str,
        tools: List[Any] = None,
        model: str = "gpt-4o-mini",
    ):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent
            instructions: Instructions for the agent (System Prompt)
            tools: List of tools available to the agent
            model: Model to use for the agent (default: "gpt-4o-mini")
        """
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.model = model
        self.agent = self._create_agent()

    def _create_agent(self) -> CodeAgent:
        """Create the code agent with tools and system prompt."""
        return Agent(
            name=self.name,
            instructions=self.instructions,
            model=self.model,
            tools=self.tools,
        )
