"""Configuration settings for the Student Assistant System."""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Configuration settings class."""

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # OpenAI Model Configuration
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))

    # API Endpoints
    API_ENDPOINTS: Dict[str, str] = {"base_url": "https://api.mahanls.com"}

    # Agent System Prompts
    AGENT_PROMPTS: Dict[str, str] = {
        "academic": """You are an Academic Assistant Agent. You help students with:
        - Checking grades and academic performance
        - Managing assignments and deadlines
        - Getting course information
        - Submitting assignments
        Always provide clear, helpful responses about academic matters.""",
        "schedule": """You are a Schedule Management Agent. You help students with:
        - Viewing class schedules and timetables
        - Booking rooms and facilities
        - Finding campus events
        - Checking availability of resources
        Provide organized, time-sensitive information.""",
        "resource": """You are a Resource Management Agent. You help students with:
        - Finding library books and materials
        - Accessing study resources
        - Checking equipment availability
        - Making reservations
        Focus on helping students find and access academic resources.""",
        "support": """You are a Student Support Agent. You help students with:
        - General inquiries about services
        - Contact information for departments
        - Submitting help requests
        - Campus announcements and news
        Be supportive and guide students to the right resources.""",
    }

    # Validation
    def validate(self) -> None:
        """Validate critical settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")

        if not self.OPENAI_MODEL:
            raise ValueError("OPENAI_MODEL is required")


# Global settings instance
settings = Settings()
settings.validate()
