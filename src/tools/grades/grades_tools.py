from agents import function_tool
import requests
from src.config.settings import settings
from typing import List


@function_tool
def get_all_grades() -> List:
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """
    Get a list of all available grades. You can access all the available grades using this tool. In case the user asks for grades or the user question is related to grades, each grade is constructed as follows: id, user, lesson, total_score, score, nomrehozoor (which is the grade for being absent/present). 
    """
    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url'
            ]}/external-services/api/v1/grades/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_lesson_grades(lesson_id: str) -> List:
    """Get a list of all grades for a specific lesson. You have to pass the lesson id as a query parameter in the request. Use this tool in case the user asks for grades in a specific lesson. In case you the user add lesson name to the question, use the lessons tool to get the lesson id and pass it to this tool. In case you could not find the lesson id, respond back to the user that the lesson is not found.

    Args:
        lesson_id (str): The id of the lesson.
    """

    try:

        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/grades/",
            params={"lesson": lesson_id},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_student_grades(student_id: str) -> List:
    """Get a list of all grades for a specific student. You have to pass the student id as a query parameter in the request. Use this tool in case the user asks for him/her or another student grades. In case you the user use student name in the question, use the Students Agent to find the student id and pass it to this tool. In case you could not find the student id, respond back to the user that the user is not found or that the user does not exist.

    Args:
        student_id (str): The id of the student.
    """

    try:

        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/grades/",
            params={"user": student_id},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}
