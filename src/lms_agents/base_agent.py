from abc import ABC, abstractmethod
from typing import List, Any, Optional, Dict
from dataclasses import dataclass
from functools import lru_cache
import logging
from agents import Agent
from smolagents import LiteLLMModel, CodeAgent
from src.config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Standardized response format for all agents."""

    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(
        self,
        name: str,
        instructions: str,
        tools: List[Any] = None,
        model: str = "gpt-4o-mini",
        cache_enabled: bool = True,
    ):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent
            instructions: Instructions for the agent (System Prompt)
            tools: List of tools available to the agent
            model: Model to use for the agent
            cache_enabled: Whether to enable response caching
        """
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.model = model
        self.cache_enabled = cache_enabled
        self.agent = self._create_agent()
        logger.info(f"Initialized {name} with {len(self.tools)} tools")

    def _create_agent(self) -> CodeAgent:
        """Create the code agent with tools and system prompt."""
        return Agent(
            name=self.name,
            instructions=self.instructions,
            model=self.model,
            tools=self.tools,
        )

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides."""
        pass
