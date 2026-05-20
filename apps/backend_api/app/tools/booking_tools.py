import uuid
from datetime import datetime
from typing import Optional

def generate_booking_id() -> str:
    """Generate a unique booking ID."""
    return f"HS-{str(uuid.uuid4())[:8].upper()}"


def create_booking_record(
    service_type: str,
    issue: str,
    priority: str,
    provider_id: str,
    provider_name: str,
    provider_phone: str,
    provider_address: str,
    user_id: str,
    confirmed_time: str,
) -> dict:
    """
    Create a complete booking record.

    Args:
        service_type: Type of service (e.g., Plumbing)
        issue: Short issue description
        priority: HIGH/MEDIUM/LOW
        provider_id: Provider's unique ID
        provider_name: Provider display name
        provider_phone: Provider contact number
        provider_address: Provider's address
        user_id: User's ID or session ID
        confirmed_time: Confirmed appointment time (ISO datetime)

    Returns:
        Complete booking record dict
    """
    duration_map = {
        "Plumbing": 60, "Electrical": 120, "AC/HVAC": 90,
        "Gas/Geyser": 60, "Appliance Repair": 90, "Cleaning": 120,
        "Pest Control": 90, "Painting": 240, "Carpentry": 120,
    }
    cost_map = {
        "Plumbing": (500, 2000), "Electrical": (1000, 5000),
        "AC/HVAC": (1500, 6000), "Gas/Geyser": (800, 3000),
        "Appliance Repair": (1000, 4000), "Cleaning": (2000, 8000),
    }

    duration = duration_map.get(service_type, 90)
    cost_range = cost_map.get(service_type, (1000, 5000))

    return {
        "booking_id": generate_booking_id(),
        "service_type": service_type,
        "issue": issue,
        "priority": priority,
        "provider_id": provider_id,
        "provider_name": provider_name,
        "provider_phone": provider_phone,
        "provider_address": provider_address,
        "user_id": user_id,
        "confirmed_time": confirmed_time,
        "estimated_duration_minutes": duration,
        "estimated_cost_pkr_min": cost_range[0],
        "estimated_cost_pkr_max": cost_range[1],
        "status": "CONFIRMED",
        "created_at": datetime.utcnow().isoformat(),
    }


def send_confirmation(booking: dict) -> str:
    """
    Format and send booking confirmation message to user.

    Args:
        booking: BookingRecord dict

    Returns:
        Formatted confirmation message string
    """
    return (
        f"✅ Booking Confirmed!\n"
        f"Provider: {booking['provider_name']}\n"
        f"Service: {booking['service_type']} — {booking['issue']}\n"
        f"Time: {booking['confirmed_time']}\n"
        f"Estimated Cost: PKR {booking['estimated_cost_pkr_min']}–{booking['estimated_cost_pkr_max']}\n"
        f"Booking ID: {booking['booking_id']}"
    )


def schedule_reminder(booking_id: str, reminder_type: str, send_at: str) -> dict:
    """
    Schedule a reminder for the user or provider.

    Args:
        booking_id: Booking reference ID
        reminder_type: 'user_30min' | 'provider_60min' | 'completion_check'
        send_at: ISO datetime when to send the reminder

    Returns:
        Reminder confirmation dict
    """
    return {
        "booking_id": booking_id,
        "reminder_type": reminder_type,
        "scheduled_at": send_at,
        "status": "scheduled"
    }


def check_completion_status(booking_id: str) -> dict:
    """
    Poll the current completion status of a booking.

    Args:
        booking_id: Booking reference ID

    Returns:
        dict with 'status' field
    """
    # In production: query DB for job status
    return {"booking_id": booking_id, "status": "COMPLETED"}


def collect_feedback(booking_id: str, rating: int, comment: Optional[str] = None) -> dict:
    """
    Collect and store user feedback after job completion.

    Args:
        booking_id: Booking reference ID
        rating: 1–5 star rating
        comment: Optional text feedback

    Returns:
        Feedback record dict
    """
    return {
        "booking_id": booking_id,
        "rating": rating,
        "comment": comment,
        "submitted_at": datetime.utcnow().isoformat()
    }


def escalate_issue(booking_id: str, reason: str) -> dict:
    """
    Escalate a failed or disputed booking for manual resolution.

    Args:
        booking_id: Booking reference ID
        reason: Reason for escalation

    Returns:
        Escalation ticket dict
    """
    return {
        "booking_id": booking_id,
        "escalation_id": f"ESC-{str(uuid.uuid4())[:6].upper()}",
        "reason": reason,
        "status": "OPEN",
        "created_at": datetime.utcnow().isoformat()
    }
