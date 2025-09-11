from agents import function_tool
import requests
from src.config.settings import settings
import logging
from src.lms_agents.auth import auth_agent
from src.utils.utils import retry_on_failure
import time
from src.lms_agents.base_agent import AgentResponse


logger = logging.getLogger(__name__)


@function_tool
@retry_on_failure(max_retries=3)
def get_all_grades() -> AgentResponse:
    token_response = auth_agent.authenticate_user()
    if not token_response.success:
        return AgentResponse(
            success=False, error="Authentication failed: " + token_response.error
        )

    access_token = token_response.data.get("access")
    headers = {"Authorization": f"Bearer {access_token}"}
    """
    Get a list of all available grades with improved error handling. Using this tool all grade details like id, user, lesson, total_score, score, nomrehozoor (which is the grade for being absent/present), etc is available.
    Returns standardized response format.
    """

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/grades/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        grades = data.get("results", [])

        return AgentResponse(
            success=True,
            data=grades,
            metadata={"total_grades": len(grades), "timestamp": time.time()},
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch grades: {e}")
        return AgentResponse(success=False, error=f"Failed to fetch grades: {str(e)}")


@function_tool
@retry_on_failure(max_retries=3)
def get_lesson_grades(lesson_id: str) -> AgentResponse:
    """Get a list of all grades for a specific lesson. The lesson id as a query parameter in the request is required. This tool could be used in case the user asks for grades in a specific lesson. In case the user add lesson name to the question, use the lessons tool to get the lesson id and pass it to this tool. In case you could not find the lesson id, respond back to the user that the lesson is not found. Returns standardized response format.

    Args:
        lesson_id (str): The id of the lesson.
    """

    token_response = auth_agent.authenticate_user()
    if not token_response.success:
        return AgentResponse(
            success=False, error="Authentication failed: " + token_response.error
        )

    access_token = token_response.data.get("access")
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/grades/",
            timeout=10,
            params={"lesson": lesson_id},
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        lesson_grades = data.get("results", [])

        return AgentResponse(
            success=True,
            data=lesson_grades,
            metadata={
                "lesson_grades_length": len(lesson_grades),
                "timestamp": time.time(),
            },
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch lesson grades: {e}")
        return AgentResponse(
            success=False, error=f"Failed to fetch lesson grades: {str(e)}"
        )


@function_tool
@retry_on_failure(max_retries=3)
def get_student_grades(student_id: str) -> AgentResponse:
    """Get a list of all grades for a specific student. Tthe student id as a query parameter in the request is required. This tool could be used in case the user asks for him/her or another student grades. In case you the user add student name in the question, use the Students Agent to find the student id and pass it to this tool. In case you could not find the student id, respond back to the user that the user is not found or that the user does not exist. Returns standardized response format

    Args:
        student_id (str): The id of the student.
    """

    token_response = auth_agent.authenticate_user()
    if not token_response.success:
        return AgentResponse(
            success=False, error="Authentication failed: " + token_response.error
        )

    access_token = token_response.data.get("access")
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/grades/",
            timeout=10,
            params={"user": student_id},
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        user_grades = data.get("results", [])

        return AgentResponse(
            success=True,
            data=user_grades,
            metadata={
                "student_grades_length": len(user_grades),
                "timestamp": time.time(),
            },
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch lesson grades: {e}")
        return AgentResponse(
            success=False, error=f"Failed to fetch lesson grades: {str(e)}"
        )
