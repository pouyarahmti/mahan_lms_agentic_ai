"""Base agent class for the Student Assistant System."""

from abc import ABC, abstractmethod
from typing import List, Any
from smolagents import LiteLLMModel, CodeAgent
from config.settings import settings


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, agent_type: str, tools: List[Any] = None):
        """
        Initialize the base agent.

        Args:
            agent_type: Type of agent (academic, schedule, resource, support)
            tools: List of tools available to this agent
        """
        self.agent_type = agent_type
        self.tools = tools or []
        self.model = self._create_model()
        self.agent = self._create_agent()

    def _create_model(self) -> LiteLLMModel:
        """Create the LLM model for this agent."""
        return LiteLLMModel(
            model_id=f"openai/{settings.OPENAI_MODEL}",
            api_key=settings.OPENAI_API_KEY,
            api_base="https://api.openai.com/v1",
        )

    def _create_agent(self) -> CodeAgent:
        """Create the code agent with tools and system prompt."""
        return CodeAgent(
            model=self.model,
            tools=self.tools,
            system_prompt=settings.AGENT_PROMPTS.get(self.agent_type, ""),
        )

    def run(self, query: str) -> str:
        """
        Execute a query using this agent.

        Args:
            query: The user's query

        Returns:
            Agent's response
        """
        try:
            return self.agent.run(query)
        except Exception as e:
            return f"Error processing request: {str(e)}"

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return a list of capabilities this agent provides."""
        pass

    def add_tool(self, tool: Any) -> None:
        """Add a tool to this agent."""
        self.tools.append(tool)
        # Recreate agent with new tools
        self.agent = self._create_agent()

    def get_tool_names(self) -> List[str]:
        """Get names of all tools available to this agent."""
        return [
            tool.__name__ if hasattr(tool, "__name__") else str(tool)
            for tool in self.tools
        ]
