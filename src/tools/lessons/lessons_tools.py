from agents import function_tool
import requests
from src.config.settings import settings
from typing import List


@function_tool
def get_all_lessons() -> List:
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """
    Get a list of all available lessons. You can access all the available lessons using this tool. In case the user asks for all the available lessons or the user question is related to all the available lessons. 
    """
    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url'
            ]}/external-services/api/v1/lessons/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_lessons_by_course(course_id: str) -> List:
    """Get a list of all lessons for a specific course. You have to pass the course id as a query parameter in the request. Use this tool in case the user asks for lessons in a specific course. In case you the user add course name to the question, use the courses tool to get the course id and pass it to this tool. In case you could not find the course id, respond back to the user that the course is not found.

    Args:
        course_id (str): The id of the course.
    """

    try:

        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/lessons/",
            params={"course": course_id},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}
