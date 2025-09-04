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

    API_ACCESS_KEY = os.getenv("API_ACCESS_KEY")

    # API Endpoints
    API_ENDPOINTS: Dict[str, str] = {"base_url": "https://api.mahanls.com"}

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
