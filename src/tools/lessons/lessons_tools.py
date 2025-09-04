from agents import function_tool
import requests
from src.config.settings import settings
import logging
from src.utils.utils import retry_on_failure
import time
from src.lms_agents.base_agent import AgentResponse


logger = logging.getLogger(__name__)


@function_tool
@retry_on_failure(max_retries=3)
def get_all_lessons() -> AgentResponse:

    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """
    Get a list of all available lessons with improved error handling. Using this tool all lessons details like name, description, course, teacher, etc is available. 
    Returns standardized response format.
    """

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/lessons/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        lessons = data.get("results", [])

        return AgentResponse(
            success=True,
            data=lessons,
            metadata={"total_lessons": len(lessons), "timestamp": time.time()},
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch lessons: {e}")
        return AgentResponse(success=False, error=f"Failed to fetch lessons: {str(e)}")


@function_tool
@retry_on_failure(max_retries=3)
def get_lessons_by_course(course_id: str) -> AgentResponse:
    """Get lessons of a course by course id. The course id as a query parameter in the request is required. Use this tool in case you need to find a specific course lessons. In case the user adds course name in the question, use the all courses tool to get the course id and pass it to this tool. In case you could not find the course id, respond back to the user that the course is not found. Returns standardized response format.


    Args:
        course_id (str): The id of the course (must be non-empty).
    """

    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/lessons/",
            timeout=10,
            params={"course": course_id},
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        course_lessons = data.get("results", [])

        return AgentResponse(
            success=True,
            data=course_lessons,
            metadata={
                "course_lessons_length": len(course_lessons),
                "timestamp": time.time(),
            },
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch course lessons: {e}")
        return AgentResponse(
            success=False, error=f"Failed to fetch course lessons: {str(e)}"
        )
