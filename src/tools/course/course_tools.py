from agents import function_tool
import requests
from src.config.settings import settings
import time
import logging
from src.lms_agents.base_agent import AgentResponse
from src.utils.utils import retry_on_failure

logger = logging.getLogger(__name__)


@function_tool
@retry_on_failure(max_retries=3)
def get_all_courses() -> AgentResponse:
    """
    Get a list of all available courses with improved error handling.
    Returns standardized response format.
    """
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/courses/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        courses = data.get("results", [])

        return AgentResponse(
            success=True,
            data=courses,
            metadata={"total_courses": len(courses), "timestamp": time.time()},
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch courses: {e}")
        return AgentResponse(success=False, error=f"Failed to fetch courses: {str(e)}")


@function_tool
@retry_on_failure(max_retries=3)
def get_courses_by_category(category_id: str) -> AgentResponse:
    """
    Get courses by category with validation and improved error handling.

    Args:
        category_id (str): The ID of the category (must be non-empty)
    """
    if not category_id or not category_id.strip():
        return AgentResponse(success=False, error="Category ID cannot be empty")

    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/courses/",
            params={"category": category_id.strip()},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        courses = data.get("results", [])

        return AgentResponse(
            success=True,
            data=courses,
            metadata={
                "category_id": category_id,
                "course_count": len(courses),
                "timestamp": time.time(),
            },
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch courses for category {category_id}: {e}")
        return AgentResponse(
            success=False,
            error=f"Failed to fetch courses for category {category_id}: {str(e)}",
        )
