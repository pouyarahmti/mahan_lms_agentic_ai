from agents import function_tool
import requests
from src.config.settings import settings
from typing import List
import logging
from src.utils.utils import retry_on_failure
import time
from src.lms_agents.base_agent import AgentResponse


logger = logging.getLogger(__name__)


@function_tool
@retry_on_failure(max_retries=3)
def get_all_students() -> AgentResponse:
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """
    Get a list of all available students with improved error handling. Using this tool yall students details like name, phone number, contact details (email, address), job information, etc is available. 
    Returns standardized response format.
    """

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/students/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        students = data.get("results", [])

        return AgentResponse(
            success=True,
            data=students,
            metadata={"total_students": len(students), "timestamp": time.time()},
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch students: {e}")
        return AgentResponse(success=False, error=f"Failed to fetch students: {str(e)}")


@function_tool
@retry_on_failure(max_retries=3)
def get_student_by_id(student_id: str) -> AgentResponse:
    """Get a student by id. The student id as a query parameter in the request is required. Use this tool in case you need to find a specific student. In case you the user name to the question, use the all students tool to get the student id and pass it to this tool. In case you could not find the student id, respond back to the user that the student is not found.

    Args:
        student_id (str): The id of the student (must be non-empty).
    """

    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/students/{student_id}",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        student = data.get("results", [])

        return AgentResponse(
            success=True,
            data=student,
            metadata={"student": student, "timestamp": time.time()},
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch student: {e}")
        return AgentResponse(success=False, error=f"Failed to fetch student: {str(e)}")


@function_tool
@retry_on_failure(max_retries=3)
def get_student_by_name(student_name: str) -> List:
    """Get a student by name. The student name as a query parameter in the request is required. Use this tool in case you need to find a specific student by name.  In case you could not find a student with that student name, respond back to the user that the student is not found.

    Args:
        student_name (str): The name of the student (must be non-empty).
    """

    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/students/",
            timeout=10,
            params={"search": student_name},
            headers=headers,
        )
        response.raise_for_status()

        data = response.json()
        student = data.get("results", [])

        return AgentResponse(
            success=True,
            data=student,
            metadata={"student": student, "timestamp": time.time()},
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch student: {e}")
        return AgentResponse(success=False, error=f"Failed to fetch student: {str(e)}")
