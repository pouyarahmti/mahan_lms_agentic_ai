from agents import function_tool
import requests
from src.config.settings import settings
from typing import List


@function_tool
def get_all_courses() -> List:
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """
    Get a list of all available courses. You can access all the available courses using this tool. In case the user asks for all the available courses.
    """
    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url'
            ]}/external-services/api/v1/courses/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_courses_by_category(category_id: str) -> List:
    """Get a list of all courses for a specific category. You have to pass the category id as a query parameter in the request. Use this tool in case the user asks for courses in a specific category.

    Args:
        category_id (str): The id of the category.
    """

    try:

        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/courses/",
            params={"category": category_id},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}
