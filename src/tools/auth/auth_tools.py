from agents import function_tool
from src.utils.utils import retry_on_failure
import requests
from src.config.settings import settings
from src.lms_agents.base_agent import AgentResponse
import logging
import time

logger = logging.getLogger(__name__)


@retry_on_failure(max_retries=3)
def authenticate_user(username: str = None, password: str = None) -> AgentResponse:
    """
    Authenticate a user and retrieve an access token.

    If username/password not provided, uses default system credentials.
    """

    payload = {
        "national_code": username or settings.USERNAME,
        "password": password or settings.PASSWORD,
    }

    try:
        response = requests.post(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/token/",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        # Example expected structure: {"access_token": "...", "expires_in": 3600}
        token = data.get("access")

        if not token:
            return AgentResponse(
                success=False, error="Authentication succeeded but token missing"
            )

        logger.info("Authentication succeeded")

        return AgentResponse(
            success=True,
            data={"access": token, "expires_in": data.get("expires_in", 3600)},
            metadata={"timestamp": time.time()},
        )

    except requests.RequestException as e:
        logger.error(f"Authentication failed: {e}")
        return AgentResponse(success=False, error=f"Authentication failed: {str(e)}")
