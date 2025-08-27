from agents import function_tool
import requests
from src.config.settings import settings
from typing import List, Optional
import time
from functools import wraps
import logging
from src.lms_agents.base_agent import AgentResponse

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying failed API calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            
            logger.error(f"All {max_retries} attempts failed. Last error: {last_exception}")
            return AgentResponse(
                success=False, 
                error=f"API call failed after {max_retries} attempts: {str(last_exception)}"
            )
        return wrapper
    return decorator

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
            metadata={
                "total_courses": len(courses),
                "timestamp": time.time()
            }
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
        return AgentResponse(
            success=False, 
            error="Category ID cannot be empty"
        )
    
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
                "timestamp": time.time()
            }
        )
    except requests.RequestException as e:
        logger.error(f"Failed to fetch courses for category {category_id}: {e}")
        return AgentResponse(
            success=False, 
            error=f"Failed to fetch courses for category {category_id}: {str(e)}"
        )
