from agents import function_tool
import requests
from src.config.settings import settings
from typing import List
import logging
from src.lms_agents.auth import auth_agent
from src.utils.utils import retry_on_failure
import time
from src.lms_agents.base_agent import AgentResponse


logger = logging.getLogger(__name__)


@function_tool
@retry_on_failure(max_retries=3)
def get_all_homeworks() -> AgentResponse:

    token_response = auth_agent.authenticate_user()
    if not token_response.success:
        return AgentResponse(
            success=False, error="Authentication failed: " + token_response.error
        )

    access_token = token_response.data.get("access")
    headers = {"Authorization": f"Bearer {access_token}"}

    """
    Get a list of all available homeworks with improved error handling. Using this tool all homework details like name, ..., etc is available. 
    Returns standardized response format.
    """

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/homeworks/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        homeworks = data.get("results", [])

        return AgentResponse(
            success=True,
            data=homeworks,
            metadata={"total_homeworks": len(homeworks), "timestamp": time.time()},
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch homeworks: {e}")
        return AgentResponse(
            success=False, error=f"Failed to fetch homeworks: {str(e)}"
        )


@function_tool
@retry_on_failure(max_retries=3)
def get_all_homework_responses() -> AgentResponse:

    token_response = auth_agent.authenticate_user()
    if not token_response.success:
        return AgentResponse(
            success=False, error="Authentication failed: " + token_response.error
        )

    access_token = token_response.data.get("access")
    headers = {"Authorization": f"Bearer {access_token}"}

    """
    Get a list of all available homework responses with improved error handling. Using this tool all homework details like name, homework, ..., etc is available. 
    Returns standardized response format.
    """

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/homework-responses/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        homework_responses = data.get("results", [])

        return AgentResponse(
            success=True,
            data=homework_responses,
            metadata={
                "total_homeworks_responses": len(homework_responses),
                "timestamp": time.time(),
            },
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch homework responses: {e}")
        return AgentResponse(
            success=False, error=f"Failed to fetch homework responses: {str(e)}"
        )


@function_tool
@retry_on_failure(max_retries=3)
def get_all_homework_responses_by_homework(homework_id: str) -> AgentResponse:
    """Get a list of all homeworks responses for a specific homework. The homework id as a query parameter in the request is required. Use this tool in case you need to find all homeworks responses for a specific homework.  In case you could not find a homework with that homework id, respond back to the user that the homework is not found. Returns standardized response format.


    Args:
        homework_id (str): The id of the homework (must be non-empty).
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
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/homework-responses/",
            timeout=10,
            params={"homework": homework_id},
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        homework_responses_by_homework = data.get("results", [])

        return AgentResponse(
            success=True,
            data=homework_responses_by_homework,
            metadata={
                "total_homework_responses": len(homework_responses_by_homework),
                "timestamp": time.time(),
            },
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch homework responses by homework: {e}")
        return AgentResponse(
            success=False,
            error=f"Failed to fetch homework responses by homework: {str(e)}",
        )


@function_tool
@retry_on_failure(max_retries=3)
def get_homeworks_by_lesson(lesson_id: str) -> AgentResponse:
    """Get a list of all homeworks for a specific lesson. The lesson id as a query parameter in the request is required. Use this tool in case you need to find all homeworks  for a specific lesson.  In case you could not find a lesson with that lesson id, respond back to the user that the lesson is not found. Returns standardized response format.


    Args:
        lesson_id (str): The id of the lesson (must be non-empty).
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
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/homeworks/",
            timeout=10,
            params={"lesson": lesson_id},
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        homeworks_by_lesson = data.get("results", [])

        return AgentResponse(
            success=True,
            data=homeworks_by_lesson,
            metadata={
                "total_homeworks": len(homeworks_by_lesson),
                "timestamp": time.time(),
            },
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch homeworks by lesson: {e}")
        return AgentResponse(
            success=False,
            error=f"Failed to fetch homeworks by lesson: {str(e)}",
        )


@function_tool
@retry_on_failure(max_retries=3)
def get_homeworks_responses_by_user(student_id: str) -> AgentResponse:
    """Get a list of all homeworks responses for a specific student. The student id as a query parameter in the request is required. Use this tool in case you need to find all homeworks responses for a specific student.  In case you could not find a student with that student id, respond back to the user that the student is not found. Returns standardized response format.


    Args:
        student_id (str): The id of the student (must be non-empty).
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
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/homework-responses/",
            timeout=10,
            params={"user": student_id},
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        homework_responses_by_student = data.get("results", [])

        return AgentResponse(
            success=True,
            data=homework_responses_by_student,
            metadata={
                "total_homework_responses_by_student": len(
                    homework_responses_by_student
                ),
                "timestamp": time.time(),
            },
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch homework responses by student: {e}")
        return AgentResponse(
            success=False,
            error=f"Failed to fetch homework responses by student: {str(e)}",
        )
