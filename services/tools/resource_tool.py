"""Resource tools for the Student Assistant System."""

import json
from datetime import datetime, timedelta
from smolagents import tool
from services.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)
api_client = APIClient()

@tool
def search_library(query: str, resource_type: str = "all", limit: int = 10) -> str:
    """
    Search library resources.
    
    Args:
        query: Search query
        resource_type: Type of resource (books, journals, digital, equipment, all)
        limit: Maximum number of results
    """
    try:
        logger.info(f"Searching library for: {query}")
        
        endpoint = "library/search"
        params = {
            "q": query,
            "type": resource_type,
            "limit": limit
        }
        
        if api_client.is_mock_mode():
            mock_response = {
                "query": query,
                "resource_type": resource_type,
                "results": [
                    {
                        "id": "B001",
                        "title": "Data Structures and Algorithms in Python",
                        "author": "Michael T. Goodrich",
                        "type": "book",
                        "isbn": "978-1118290279",
                        "availability": "available",
                        "location": "CS Section, Floor 2, Shelf 15-A",
                        "call_number": "QA76.73.P98 G66 2013",
                        "due_date": None,
                        "copies_available": 3,
                        "copies_total": 5,
                        "format": "Physical"
                    },
                    {
                        "id": "J001",
                        "title": "Journal of Computer Science and Technology",
                        "type": "journal",
                        "availability": "digital",
                        "access_url": "https://library.university.edu/digital/jcst",
                        "database": "IEEE Xplore",
                        "years_available": "1995-present",
                        "format": "Digital"
                    },
                    {
                        "id": "E001",
                        "title": "Laptop - Dell Latitude 5520",
                        "type": "equipment",
                        "availability": "available",
                        "location": "Library Service Desk",
                        "loan_period": "7 days",
                        "specifications": {
                            "processor": "Intel i5",
                            "ram": "8GB",
                            "storage": "256GB SSD",
                            "os": "Windows 11"
                        },
                        "accessories": ["charger", "laptop_bag"],
                        "condition": "excellent"
                    }
                ],
                "total_results": 3,
                "search_time": "0.23 seconds"
            }
        else:
            response = api_client.get(endpoint, params=params, api_type="library")
            mock_response = response.json() if response.status_code == 200 else {"error": "Search failed"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error searching library: {str(e)}")
        return f"Error searching library: {str(e)}"

@tool
def get_study_materials(course_code: str, material_type: str = "all", semester: str = None) -> str:
    """
    Get study materials for a course.
    
    Args:
        course_code: Course code
        material_type: Type of material (slides, notes, assignments, readings, all)
        semester: Specific semester filter
    """
    try:
        logger.info(f"Getting study materials for {course_code}")
        
        endpoint = f"library/course-materials/{course_code}"
        params = {"type": material_type}
        
        if semester:
            params["semester"] = semester
        
        if api_client.is_mock_mode():
            mock_response = {
                "course_code": course_code,
                "course_title": "Introduction to Computer Science",
                "semester": semester or "Fall 2024",
                "materials": [
                    {
                        "id": "M001",
                        "title": "Lecture 10: Binary Trees and BST",
                        "type": "slides",
                        "upload_date": "2024-12-10",
                        "file_size": "2.3 MB",
                        "format": "PDF",
                        "url": "https://lms.university.edu/cs101/slides/lecture10.pdf",
                        "instructor": "Dr. Smith",
                        "topics": ["Binary Trees", "Binary Search Trees", "Tree Traversal"]
                    },
                    {
                        "id": "M002",
                        "title": "Final Exam Study Guide",
                        "type": "notes",
                        "upload_date": "2024-12-12",
                        "file_size": "1.8 MB",
                        "format": "PDF",
                        "url": "https://lms.university.edu/cs101/notes/final_guide.pdf",
                        "instructor": "Dr. Smith",
                        "topics": ["All major topics", "Sample problems", "Key concepts"]
                    },
                    {
                        "id": "M003",
                        "title": "Assignment 5: Tree Implementation",
                        "type": "assignment",
                        "upload_date": "2024-12-08",
                        "due_date": "2024-12-20",
                        "file_size": "0.5 MB",
                        "format": "PDF",
                        "url": "https://lms.university.edu/cs101/assignments/assignment5.pdf",
                        "points": 100,
                        "status": "active"
                    },
                    {
                        "id": "M004",
                        "title": "Required Reading: Chapter 8 - Trees",
                        "type": "reading",
                        "source": "Data Structures Textbook",
                        "pages": "pp. 234-267",
                        "digital_copy": "https://library.university.edu/ebooks/ds_textbook/chapter8",
                        "topics": ["Tree basics", "Implementation", "Applications"]
                    }
                ],
                "total_materials": 4,
                "last_updated": "2024-12-12"
            }
        else:
            response = api_client.get(endpoint, params=params, api_type="library")
            mock_response = response.json() if response.status_code == 200 else {"error": "Materials not found"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error retrieving study materials: {str(e)}")
        return f"Error retrieving study materials: {str(e)}"

@tool
def check_resource_availability(resource_id: str, date: str = None) -> str:
    """
    Check if a specific resource is available.
    
    Args:
        resource_id: Resource identifier
        date: Optional date to check (YYYY-MM-DD)
    """
    try:
        logger.info(f"Checking availability for resource {resource_id}")
        
        endpoint = f"library/resources/{resource_id}/availability"
        params = {}
        
        if date:
            params["date"] = date
        
        if api_client.is_mock_mode():
            mock_response = {
                "resource_id": resource_id,
                "name": "MacBook Pro 13-inch",
                "type": "equipment",
                "category": "laptop",
                "current_status": "available",
                "location": "Library Technology Desk",
                "loan_details": {
                    "max_loan_period": "7 days",
                    "renewable": True,
                    "max_renewals": 2,
                    "fine_per_day": "$5.00"
                },
                "specifications": {
                    "model": "MacBook Pro 13-inch M2",
                    "processor": "Apple M2 chip",
                    "memory": "8GB unified memory",
                    "storage": "256GB SSD",
                    "os": "macOS Ventura"
                },
                "accessories_included": [
                    "MagSafe 3 charger",
                    "USB-C to MagSafe 3 cable",
                    "Protective sleeve"
                ],
                "condition": "excellent",
                "last_maintenance": "2024-11-15",
                "next_available": "immediately",
                "reservation_queue": [],
                "upcoming_reservations": [
                    {
                        "date": "2024-12-18",
                        "time": "14:00-16:00",
                        "student": "STU_456"
                    }
                ]
            }
        else:
            response = api_client.get(endpoint, params=params, api_type="library")
            mock_response = response.json() if response.status_code == 200 else {"error": "Resource not found"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error checking resource availability: {str(e)}")
        return f"Error checking resource availability: {str(e)}"

@tool
def reserve_resource(student_id: str, resource_id: str, date_from: str, 
                    date_to: str = None, purpose: str = "") -> str:
    """
    Reserve a resource for a student.
    
    Args:
        student_id: Student's ID
        resource_id: Resource identifier
        date_from: Start date (YYYY-MM-DD) or datetime (YYYY-MM-DD HH:MM)
        date_to: End date (YYYY-MM-DD) or datetime, optional for equipment
        purpose: Purpose of reservation
    """
    try:
        logger.info(f"Reserving resource {resource_id} for student {student_id}")
        
        endpoint = "library/reservations"
        payload = {
            "student_id": student_id,
            "resource_id": resource_id,
            "date_from": date_from,
            "date_to": date_to,
            "purpose": purpose,
            "reservation_time": datetime.now().isoformat()
        }
        
        if api_client.is_mock_mode():
            reservation_id = f"RES_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            mock_response = {
                "reservation_id": reservation_id,
                "status": "confirmed",
                "resource": {
                    "id": resource_id,
                    "name": "MacBook Pro 13-inch",
                    "type": "equipment"
                },
                "reservation_details": {
                    "student_id": student_id,
                    "date_from": date_from,
                    "date_to": date_to or date_from,
                    "purpose": purpose,
                    "duration": "7 days" if not date_to else "Custom period"
                },
                "pickup_info": {
                    "location": "Library Technology Desk",
                    "hours": "Mon-Fri 8:00-20:00, Sat-Sun 10:00-18:00",
                    "id_required": True,
                    "contact": "tech-desk@university.edu"
                },
                "policies": {
                    "late_return_fee": "$5.00 per day",
                    "damage_policy": "Full replacement cost if damaged",
                    "renewal_possible": True,
                    "cancellation_deadline": "2 hours before pickup"
                },
                "confirmation_email": "sent",
                "qr_code": f"https://university.edu/reservations/qr/{reservation_id}",
                "estimated_pickup_time": "15 minutes"
            }
        else:
            response = api_client.post(endpoint, data=payload, api_type="library")
            mock_response = response.json() if response.status_code == 200 else {"error": "Reservation failed"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error reserving resource: {str(e)}")
        return f"Error reserving resource: {str(e)}"

@tool
def get_digital_resources(subject: str = None, database: str = None) -> str:
    """
    Get information about digital resources and databases.
    
    Args:
        subject: Subject area filter
        database: Specific database name
    """
    try:
        logger.info(f"Getting digital resources for subject: {subject}")
        
        endpoint = "library/digital-resources"
        params = {}
        
        if subject:
            params["subject"] = subject
        if database:
            params["database"] = database
        
        if api_client.is_mock_mode():
            mock_response = {
                "digital_resources": [
                    {
                        "name": "IEEE Xplore Digital Library",
                        "type": "database",
                        "subjects": ["Computer Science", "Engineering", "Technology"],
                        "description": "IEEE's digital library providing access to technical literature",
                        "access_url": "https://ieeexplore.ieee.org",
                        "content_types": ["journals", "conference_papers", "standards"],
                        "simultaneous_users": "unlimited",
                        "remote_access": True,
                        "help_guide": "https://library.university.edu/guides/ieee"
                    },
                    {
                        "name": "ACM Digital Library",
                        "type": "database", 
                        "subjects": ["Computer Science", "Information Technology"],
                        "description": "ACM's comprehensive database of computing literature",
                        "access_url": "https://dl.acm.org",
                        "content_types": ["journals", "magazines", "conference_proceedings"],
                        "simultaneous_users": 50,
                        "remote_access": True,
                        "help_guide": "https://library.university.edu/guides/acm"
                    },
                    {
                        "name": "O'Reilly Learning Platform",
                        "type": "ebook_platform",
                        "subjects": ["Technology", "Business", "Design"],
                        "description": "Online learning platform with tech books and courses",
                        "access_url": "https://learning.oreilly.com",
                        "content_types": ["ebooks", "videos", "interactive_tutorials"],
                        "simultaneous_users": 25,
                        "remote_access": True,
                        "mobile_app": True,
                        "help_guide": "https://library.university.edu/guides/oreilly"
                    },
                    {
                        "name": "University Digital Archives",
                        "type": "repository",
                        "subjects": ["All subjects"],
                        "description": "University's institutional repository of theses and research",
                        "access_url": "https://archives.university.edu",
                        "content_types": ["theses", "dissertations", "faculty_papers"],
                        "simultaneous_users": "unlimited",
                        "remote_access": True,
                        "open_access": True
                    }
                ],
                "total_resources": 4,
                "access_instructions": {
                    "on_campus": "Direct access from any campus computer",
                    "off_campus": "Login with university credentials",
                    "troubleshooting": "Contact library-help@university.edu"
                }
            }
        else:
            response = api_client.get(endpoint, params=params, api_type="library")
            mock_response = response.json() if response.status_code == 200 else {"error": "Resources not available"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error getting digital resources: {str(e)}")
        return f"Error getting digital resources: {str(e)}"