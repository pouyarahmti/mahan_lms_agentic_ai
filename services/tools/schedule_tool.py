"""Schedule tools for the Student Assistant System."""

import json
from datetime import datetime, timedelta
from smolagents import tool
from services.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)
api_client = APIClient()

@tool
def get_schedule(student_id: str, date: str = None, view_type: str = "day") -> str:
    """
    Get student's class schedule.
    
    Args:
        student_id: The student's ID
        date: Specific date (YYYY-MM-DD), defaults to today
        view_type: Schedule view (day, week, month)
    """
    try:
        logger.info(f"Fetching schedule for student {student_id}")
        
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        endpoint = f"schedule/student/{student_id}"
        params = {"date": date, "view": view_type}
        
        if api_client.is_mock_mode():
            mock_response = {
                "student_id": student_id,
                "date": date,
                "view_type": view_type,
                "schedule": [
                    {
                        "time": "09:00-10:30",
                        "course": "CS101", 
                        "title": "Introduction to Computer Science",
                        "location": "Science Building 201",
                        "instructor": "Dr. Smith",
                        "type": "Lecture",
                        "room_capacity": 50,
                        "notes": "Bring laptop"
                    },
                    {
                        "time": "11:00-12:30",
                        "course": "MATH201",
                        "title": "Calculus II",
                        "location": "Math Building 105", 
                        "instructor": "Prof. Johnson",
                        "type": "Tutorial",
                        "room_capacity": 25,
                        "notes": "Quiz today"
                    },
                    {
                        "time": "14:00-15:30",
                        "course": "ENG102",
                        "title": "English Composition",
                        "location": "Humanities 302",
                        "instructor": "Dr. Williams",
                        "type": "Seminar",
                        "room_capacity": 20,
                        "notes": ""
                    }
                ],
                "total_classes": 3,
                "free_periods": [
                    {"time": "10:30-11:00", "duration": "30 minutes"},
                    {"time": "12:30-14:00", "duration": "1.5 hours"}
                ]
            }
        else:
            response = api_client.get(endpoint, params=params, api_type="schedule")
            mock_response = response.json() if response.status_code == 200 else {"error": "Schedule not found"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error retrieving schedule: {str(e)}")
        return f"Error retrieving schedule: {str(e)}"

@tool
def book_room(student_id: str, room_id: str, date: str, start_time: str, 
              end_time: str, purpose: str, attendees: int = 1) -> str:
    """
    Book a study room or facility.
    
    Args:
        student_id: The student's ID
        room_id: Room identifier
        date: Date for booking (YYYY-MM-DD)
        start_time: Start time (HH:MM)
        end_time: End time (HH:MM)
        purpose: Purpose of booking
        attendees: Number of attendees
    """
    try:
        logger.info(f"Booking room {room_id} for student {student_id}")
        
        endpoint = "schedule/bookings"
        payload = {
            "student_id": student_id,
            "room_id": room_id,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "purpose": purpose,
            "attendees": attendees,
            "booking_time": datetime.now().isoformat()
        }
        
        if api_client.is_mock_mode():
            booking_id = f"BOOK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            mock_response = {
                "booking_id": booking_id,
                "status": "confirmed",
                "room": {
                    "id": room_id,
                    "name": f"Study Room {room_id}",
                    "building": "Library",
                    "floor": 2,
                    "capacity": 6,
                    "equipment": ["whiteboard", "projector", "wifi"]
                },
                "booking_details": {
                    "date": date,
                    "time": f"{start_time}-{end_time}",
                    "duration": "2 hours",
                    "purpose": purpose,
                    "attendees": attendees
                },
                "access_info": {
                    "access_code": "1234",
                    "instructions": "Room will unlock 15 minutes before start time"
                },
                "confirmation": "Room successfully booked",
                "cancellation_policy": "Cancel up to 2 hours before start time"
            }
        else:
            response = api_client.post(endpoint, data=payload, api_type="schedule")
            mock_response = response.json() if response.status_code == 200 else {"error": "Booking failed"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error booking room: {str(e)}")
        return f"Error booking room: {str(e)}"

@tool
def get_events(date_from: str = None, date_to: str = None, 
               category: str = None, limit: int = 10) -> str:
    """
    Get campus events and activities.
    
    Args:
        date_from: Start date filter (YYYY-MM-DD)
        date_to: End date filter (YYYY-MM-DD)
        category: Event category filter
        limit: Maximum number of events to return
    """
    try:
        logger.info("Fetching campus events")
        
        endpoint = "schedule/events"
        params = {"limit": limit}
        
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        if category:
            params["category"] = category
        
        if api_client.is_mock_mode():
            mock_response = {
                "events": [
                    {
                        "id": "E001",
                        "title": "Career Fair 2024",
                        "date": "2024-12-20",
                        "time": "10:00-16:00",
                        "location": "Student Center Main Hall",
                        "building": "Student Center",
                        "room": "Main Hall",
                        "category": "Career",
                        "description": "Annual career fair featuring 50+ tech companies",
                        "organizer": "Career Services",
                        "registration_required": True,
                        "registration_url": "https://university.edu/events/career-fair",
                        "capacity": 500,
                        "cost": "Free"
                    },
                    {
                        "id": "E002", 
                        "title": "Winter Concert",
                        "date": "2024-12-22",
                        "time": "19:00-21:00",
                        "location": "University Auditorium",
                        "building": "Arts Center",
                        "room": "Main Auditorium",
                        "category": "Cultural",
                        "description": "Student orchestra winter performance featuring classical and contemporary pieces",
                        "organizer": "Music Department",
                        "registration_required": False,
                        "capacity": 300,
                        "cost": "$5 students, $10 general"
                    },
                    {
                        "id": "E003",
                        "title": "Study Skills Workshop",
                        "date": "2024-12-18",
                        "time": "14:00-16:00", 
                        "location": "Library Conference Room A",
                        "building": "Library",
                        "room": "Conference Room A",
                        "category": "Academic",
                        "description": "Learn effective study techniques for final exams",
                        "organizer": "Academic Success Center",
                        "registration_required": True,
                        "registration_url": "https://university.edu/workshops/study-skills",
                        "capacity": 30,
                        "cost": "Free"
                    }
                ],
                "total_events": 3,
                "filters_applied": {
                    "date_from": date_from,
                    "date_to": date_to,
                    "category": category
                }
            }
        else:
            response = api_client.get(endpoint, params=params, api_type="schedule")
            mock_response = response.json() if response.status_code == 200 else {"error": "Failed to fetch events"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error retrieving events: {str(e)}")
        return f"Error retrieving events: {str(e)}"

@tool
def check_availability(resource_type: str, date: str, start_time: str = None, 
                      end_time: str = None, building: str = None) -> str:
    """
    Check availability of rooms, equipment, or facilities.
    
    Args:
        resource_type: Type of resource (room, equipment, facility)
        date: Date to check (YYYY-MM-DD)
        start_time: Optional start time (HH:MM)
        end_time: Optional end time (HH:MM)
        building: Optional building filter
    """
    try:
        logger.info(f"Checking availability for {resource_type} on {date}")
        
        endpoint = "schedule/availability"
        params = {
            "resource_type": resource_type,
            "date": date
        }
        
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if building:
            params["building"] = building
        
        if api_client.is_mock_mode():
            mock_response = {
                "resource_type": resource_type,
                "date": date,
                "building": building,
                "available_resources": [
                    {
                        "id": "ROOM_A101",
                        "name": "Study Room A101",
                        "type": "study_room",
                        "building": "Library",
                        "floor": 1,
                        "capacity": 4,
                        "equipment": ["whiteboard", "wifi"],
                        "available_slots": [
                            {"start": "09:00", "end": "11:00"},
                            {"start": "13:00", "end": "15:00"},
                            {"start": "16:00", "end": "18:00"}
                        ]
                    },
                    {
                        "id": "ROOM_A102",
                        "name": "Conference Room A102", 
                        "type": "conference_room",
                        "building": "Library",
                        "floor": 1,
                        "capacity": 8,
                        "equipment": ["projector", "whiteboard", "video_conf", "wifi"],
                        "available_slots": [
                            {"start": "08:00", "end": "10:00"},
                            {"start": "14:00", "end": "17:00"}
                        ]
                    }
                ],
                "total_available": 2,
                "booking_instructions": "Use the booking system to reserve any available slot"
            }
        else:
            response = api_client.get(endpoint, params=params, api_type="schedule")
            mock_response = response.json() if response.status_code == 200 else {"error": "Availability check failed"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error checking availability: {str(e)}")
        return f"Error checking availability: {str(e)}"

@tool
def cancel_booking(student_id: str, booking_id: str, reason: str = "") -> str:
    """
    Cancel an existing booking.
    
    Args:
        student_id: The student's ID
        booking_id: Booking identifier to cancel
        reason: Optional reason for cancellation
    """
    try:
        logger.info(f"Cancelling booking {booking_id} for student {student_id}")
        
        endpoint = f"schedule/bookings/{booking_id}/cancel"
        payload = {
            "student_id": student_id,
            "reason": reason,
            "cancelled_at": datetime.now().isoformat()
        }
        
        if api_client.is_mock_mode():
            mock_response = {
                "booking_id": booking_id,
                "status": "cancelled",
                "cancellation_time": datetime.now().isoformat(),
                "reason": reason,
                "refund_info": {
                    "refund_applicable": True,
                    "refund_amount": 0,  # Free booking
                    "refund_method": "N/A"
                },
                "message": "Booking cancelled successfully"
            }
        else:
            response = api_client.put(endpoint, data=payload, api_type="schedule")
            mock_response = response.json() if response.status_code == 200 else {"error": "Cancellation failed"}
        
        return json.dumps(mock_response, indent=2)
        
    except Exception as e:
        logger.error(f"Error cancelling booking: {str(e)}")
        return f"Error cancelling booking: {str(e)}"