from agents import function_tool
import requests
from src.config.settings import settings
from typing import List


@function_tool
def get_all_homeworks() -> List:
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """
    Get a list of all available homeworks. You can access all the available homeworks using this tool. In case the user asks for the available homeworks or the user question is related to available homeworks. 
    """
    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url'
            ]}/external-services/api/v1/homeworks/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_all_homework_responses() -> List:
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """
    Get a list of all responses for a specific homework. You can access all the available homeworks responses using this tool. In case the user asks for the responses of a specific homework or the user question is related to a specific homework responses. 
    """
    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url'
            ]}/external-services/api/v1/homework-responses/",
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_all_homework_responses_by_homework(homework_id: str) -> List:
    headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

    """Get a list of all homeworks responses for a specific homework. You have to pass the homework id as a query parameter in the request. Use this tool in case the user asks for homeworks responses in a specific homework. In case you could not find the homework id, respond back to the user that the homework is not found.

    Args:
        homework_id (str): The id of the homework.
    """
    try:
        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url'
            ]}/external-services/api/v1/homework-responses/",
            params={"homework": homework_id},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_homeworks_by_lesson(lesson_id: str) -> List:
    """Get a list of all homeworks for a specific lesson. You have to pass the lesson id as a query parameter in the request. Use this tool in case the user asks for homeworks in a specific lesson. In case you the user add lesson name to the question, use the lessons tool to get the lesson id and pass it to this tool. In case you could not find the lesson id, respond back to the user that the lesson is not found.

    Args:
        lesson_id (str): The id of the lesson.
    """

    try:

        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/homeworks/",
            params={"lesson": lesson_id},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}


@function_tool
def get_homeworks_responses_by_user(user_id: str) -> List:
    """Get a list of all homeworks responses for a specific user. You have to pass the user id as a query parameter in the request. Use this tool in case the user asks for homeworks for a specific user. In case you the user add username to the question, use the users tool to get the user id and pass it to this tool. In case you could not find the user id, respond back to the user that the user is not found.

    Args:
        user_id (str): The id of the user.
    """

    try:

        headers = {"Authorization": f"Bearer {settings.API_ACCESS_KEY}"}

        response = requests.get(
            f"{settings.API_ENDPOINTS['base_url']}/external-services/api/v1/homework-responses/",
            params={"user": user_id},
            timeout=10,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["results"]
    except requests.RequestException as e:
        return {"error": str(e)}
