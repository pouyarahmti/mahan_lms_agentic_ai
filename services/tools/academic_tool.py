"""Academic tools for the Student Assistant System."""

import json
from datetime import datetime
from smolagents import tool
from services.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)
api_client = APIClient()

@tool
def get_grades(student_id: str, course_code: str = None) -> str:
    """
    Retrieve student grades from the academic system.
    
    Args:
        student_id: The student's ID
        course_code: Optional specific course code to filter grades
    """
    try:
        logger.info(f"Fetching grades for student {student_id}, course: {course_code}")
        
        endpoint = "academic/grades"
        params = {"student_id": student_id}
        
        if course_code:
            params["course_code"] = course_code
        
        # Use API client or mock data
        if api_client.is_mock_mode():
            mock_response = {
                "student_id": student_id,
                "grades": [
                    {"course": "CS101", "grade": "A", "credits": 3, "semester": "Fall 2024"},
                    {"course": "MATH201", "grade": "B+", "credits": 4, "semester": "Fall 2024"},
                    {"course": "ENG102", "grade": "A-", "credits": 3, "semester": "Fall 2024"}
                ],
                "gpa": 3.67,
                "total_credits": 10
            }
            
            if course_code:
                mock_response["grades"] = [
                    grade for grade in mock_response["grades"] 
                    if grade["course"] == course_code
                ]
        else:
            response = api_client.get(endpoint, params=params, api_type="academic")
            mock_response = response.json() if response.status_code == 200 else {"error": "Failed to fetch grades"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error retrieving grades: {str(e)}")
        return f"Error retrieving grades: {str(e)}"

@tool
def get_assignments(student_id: str, course_code: str = None, status: str = "pending") -> str:
    """
    Get assignments for a student.
    
    Args:
        student_id: The student's ID
        course_code: Optional specific course code
        status: Assignment status filter (pending, completed, overdue)
    """
    try:
        logger.info(f"Fetching assignments for student {student_id}")
        
        endpoint = "academic/assignments"
        params = {"student_id": student_id, "status": status}
        
        if course_code:
            params["course_code"] = course_code
        
        if api_client.is_mock_mode():
            mock_response = {
                "student_id": student_id,
                "assignments": [
                    {
                        "id": "A001",
                        "course": "CS101",
                        "title": "Data Structures Project",
                        "due_date": "2024-12-20T23:59:00",
                        "status": "pending",
                        "description": "Implement binary search tree",
                        "points": 100,
                        "submission_type": "file"
                    },
                    {
                        "id": "A002",
                        "course": "MATH201",
                        "title": "Calculus Problem Set 5",
                        "due_date": "2024-12-18T23:59:00",
                        "status": "pending",
                        "description": "Integration problems",
                        "points": 50,
                        "submission_type": "online"
                    }
                ],
                "total_assignments": 2
            }
            
            if course_code:
                mock_response["assignments"] = [
                    assignment for assignment in mock_response["assignments"]
                    if assignment["course"] == course_code
                ]
        else:
            response = api_client.get(endpoint, params=params, api_type="academic")
            mock_response = response.json() if response.status_code == 200 else {"error": "Failed to fetch assignments"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error retrieving assignments: {str(e)}")
        return f"Error retrieving assignments: {str(e)}"

@tool
def get_course_info(course_code: str) -> str:
    """
    Get detailed information about a course.
    
    Args:
        course_code: The course code (e.g., CS101)
    """
    try:
        logger.info(f"Fetching course info for {course_code}")
        
        endpoint = f"academic/courses/{course_code}"
        
        if api_client.is_mock_mode():
            mock_response = {
                "course_code": course_code,
                "title": "Introduction to Computer Science",
                "instructor": {
                    "name": "Dr. Jane Smith",
                    "email": "j.smith@university.edu",
                    "office": "CS Building Room 301",
                    "office_hours": "MW 2:00-4:00 PM"
                },
                "credits": 3,
                "schedule": {
                    "days": ["Monday", "Wednesday", "Friday"],
                    "time": "10:00-11:00 AM",
                    "location": "Science Building Room 201"
                },
                "description": "Fundamentals of programming and computer science concepts",
                "prerequisites": ["MATH101"],
                "textbook": "Introduction to Programming, 5th Edition",
                "syllabus_url": f"https://university.edu/courses/{course_code.lower()}/syllabus",
                "grading_policy": {
                    "assignments": "40%",
                    "midterm": "25%",
                    "final": "25%",
                    "participation": "10%"
                }
            }
        else:
            response = api_client.get(endpoint, api_type="academic")
            mock_response = response.json() if response.status_code == 200 else {"error": "Course not found"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error retrieving course info: {str(e)}")
        return f"Error retrieving course info: {str(e)}"

@tool
def submit_assignment(student_id: str, assignment_id: str, submission_data: str, submission_type: str = "text") -> str:
    """
    Submit an assignment for a student.
    
    Args:
        student_id: The student's ID
        assignment_id: The assignment ID
        submission_data: Assignment content or file path
        submission_type: Type of submission (text, file, url)
    """
    try:
        logger.info(f"Submitting assignment {assignment_id} for student {student_id}")
        
        endpoint = "academic/assignments/submit"
        payload = {
            "student_id": student_id,
            "assignment_id": assignment_id,
            "submission_data": submission_data,
            "submission_type": submission_type,
            "submission_time": datetime.now().isoformat()
        }
        
        if api_client.is_mock_mode():
            mock_response = {
                "status": "success",
                "message": f"Assignment {assignment_id} submitted successfully",
                "submission_id": f"SUB_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "submission_time": datetime.now().isoformat(),
                "receipt_id": "REC_001234",
                "late_penalty": 0,
                "confirmation_email_sent": True
            }
        else:
            response = api_client.post(endpoint, data=payload, api_type="academic")
            mock_response = response.json() if response.status_code == 200 else {"error": "Submission failed"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error submitting assignment: {str(e)}")
        return f"Error submitting assignment: {str(e)}"

@tool
def get_transcript(student_id: str, format_type: str = "json") -> str:
    """
    Get student's academic transcript.
    
    Args:
        student_id: The student's ID
        format_type: Format of transcript (json, pdf_url)
    """
    try:
        logger.info(f"Generating transcript for student {student_id}")
        
        endpoint = f"academic/transcript/{student_id}"
        params = {"format": format_type}
        
        if api_client.is_mock_mode():
            mock_response = {
                "student_id": student_id,
                "student_name": "John Doe",
                "program": "Bachelor of Computer Science",
                "enrollment_date": "2022-09-01",
                "expected_graduation": "2026-05-15",
                "current_gpa": 3.67,
                "total_credits": 45,
                "semesters": [
                    {
                        "semester": "Fall 2024",
                        "courses": [
                            {"course": "CS101", "title": "Intro to CS", "grade": "A", "credits": 3},
                            {"course": "MATH201", "title": "Calculus II", "grade": "B+", "credits": 4},
                            {"course": "ENG102", "title": "English Comp", "grade": "A-", "credits": 3}
                        ],
                        "semester_gpa": 3.67,
                        "semester_credits": 10
                    }
                ],
                "academic_standing": "Good Standing",
                "honors": [],
                "generated_date": datetime.now().isoformat()
            }
            
            if format_type == "pdf_url":
                mock_response["pdf_url"] = f"https://university.edu/transcripts/{student_id}.pdf"
        else:
            response = api_client.get(endpoint, params=params, api_type="academic")
            mock_response = response.json() if response.status_code == 200 else {"error": "Transcript not available"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error generating transcript: {str(e)}")
        return f"Error generating transcript: {str(e)}"