from agents import function_tool
import requests
from src.config.settings import settings
from typing import List


@function_tool
def get_all_students() -> List:
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """
    Get a list of all students. You can access all the available lessons using this tool. Using this tool you can excess all students details like name, phone number, contact details (email, address), job information, etc . 
    """
    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url'
            ]}/external-services/api/v1/students/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_student_by_id(student_id: str) -> List:
    """Get a student by id. You have to pass the students id as a query parameter in the request. Use this tool in case you need to find a specific student. In case you the user name to the question, use the all students tool to get the student id and pass it to this tool. In case you could not find the student id, respond back to the user that the student is not found.

    Args:
        student_id (str): The id of the course.
    """

    try:

        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/students/{student_id}",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_student_by_name(student_name: str) -> List:
    """Get a student by name. You have to pass the students name as a query parameter in the request. Use this tool in case you need to find a specific student name. I In case you could not find the student with the name, respond back to the user that the student not found.

    Args:
        student_name (str): The name of the student.
    """

    try:

        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/students/",
            params={"search": student_name},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}
