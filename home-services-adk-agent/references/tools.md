# Tools Reference — Home Services ADK Agent

All tools must be plain Python functions (no `async` unless needed).
ADK wraps them via `FunctionTool`. Type hints are required — ADK uses them
to auto-generate the tool schema.

---

## `tools/maps_tools.py`

```python
import httpx
import os
from typing import Optional

MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def google_maps_nearby_search(
    location: str,
    service_keyword: str,
    radius_meters: int = 5000
) -> dict:
    """
    Search for nearby service providers using Google Places Nearby Search.

    Args:
        location: Address or lat,lng string of the user's location
        service_keyword: Service type keyword (e.g., "plumber", "AC repair")
        radius_meters: Search radius in meters (default 5000)

    Returns:
        dict with 'results' list of place records
    """
    # Step 1: Geocode the location string to lat,lng
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geocode_resp = httpx.get(geocode_url, params={
        "address": location,
        "key": MAPS_API_KEY
    })
    geo_data = geocode_resp.json()

    if not geo_data.get("results"):
        return {"results": [], "error": "Location not found"}

    latlng = geo_data["results"][0]["geometry"]["location"]
    lat, lng = latlng["lat"], latlng["lng"]

    # Step 2: Nearby search for service providers
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    nearby_resp = httpx.get(nearby_url, params={
        "location": f"{lat},{lng}",
        "radius": radius_meters,
        "keyword": service_keyword,
        "key": MAPS_API_KEY
    })
    data = nearby_resp.json()

    results = []
    for place in data.get("results", []):
        results.append({
            "place_id": place.get("place_id"),
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"],
            "rating": place.get("rating", 0.0),
        })

    return {"results": results, "user_lat": lat, "user_lng": lng}


def extract_location_entity(text: str) -> Optional[str]:
    """
    Extract location entity from user text using simple heuristics.
    Returns extracted location string or None.

    Args:
        text: Raw user message

    Returns:
        Location string or None
    """
    # Common Pakistani city/area patterns
    area_keywords = [
        "DHA", "Gulshan", "Clifton", "Nazimabad", "PECHS", "Saddar",
        "Johar", "Malir", "Korangi", "Gulistan", "North Nazimabad",
        "Bahria", "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad"
    ]
    for keyword in area_keywords:
        if keyword.lower() in text.lower():
            # Try to extract full phrase around keyword
            return keyword
    return None


def calculate_distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate Haversine distance between two lat/lng points.

    Args:
        lat1, lng1: User location
        lat2, lng2: Provider location

    Returns:
        Distance in kilometers
    """
    import math
    R = 6371  # Earth radius km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng/2)**2)
    return R * 2 * math.asin(math.sqrt(a))
```

---

## `tools/db_tools.py`

```python
from typing import List, Optional
from schemas.models import ProviderRecord, AvailableSlot

# In production: replace with actual DB queries (PostgreSQL / Firebase)
# For dev/demo: use this in-memory mock

MOCK_PROVIDERS = [
    {
        "id": "p001", "name": "Usman Plumber", "category": "Plumbing",
        "address": "DHA Phase 5, Karachi", "lat": 24.8090, "lng": 67.0649,
        "phone": "+92-300-1234567", "elo_score": 1450.0, "rating": 4.7,
        "rating_count": 89, "urgency_capable": True,
        "lifecycle_completion_rate": 0.92, "response_speed_ms": 1200,
    },
    {
        "id": "p002", "name": "AC Master Karachi", "category": "AC/HVAC",
        "address": "Gulshan-e-Iqbal Block 10, Karachi", "lat": 24.9200, "lng": 67.0900,
        "phone": "+92-333-9876543", "elo_score": 1380.0, "rating": 4.5,
        "rating_count": 62, "urgency_capable": True,
        "lifecycle_completion_rate": 0.88, "response_speed_ms": 2100,
    },
]

MOCK_AVAILABILITY = {
    "p001": [
        {"slot_time": "2024-01-15T10:00:00", "duration_minutes": 60},
        {"slot_time": "2024-01-15T14:00:00", "duration_minutes": 60},
    ],
    "p002": [
        {"slot_time": "2024-01-15T11:00:00", "duration_minutes": 90},
    ],
}


def classify_service(text: str) -> str:
    """
    Classify service type from raw text.

    Args:
        text: User's message

    Returns:
        Service type string
    """
    text_lower = text.lower()
    service_map = {
        "plumb": "Plumbing", "pipe": "Plumbing", "paani": "Plumbing",
        "leak": "Plumbing", "nal": "Plumbing",
        "bijli": "Electrical", "electric": "Electrical", "wiring": "Electrical",
        "ac": "AC/HVAC", "air condition": "AC/HVAC", "cooling": "AC/HVAC",
        "geyser": "Gas/Geyser", "gas": "Gas/Geyser", "boiler": "Gas/Geyser",
        "fridge": "Appliance Repair", "washing machine": "Appliance Repair",
        "paint": "Painting", "clean": "Cleaning", "pest": "Pest Control",
        "cctv": "Internet/CCTV", "internet": "Internet/CCTV",
        "carpenter": "Carpentry", "wood": "Carpentry",
    }
    for keyword, service in service_map.items():
        if keyword in text_lower:
            return service
    return "Other"


def filter_by_category(
    providers: List[dict],
    category: str
) -> List[dict]:
    """
    Filter provider list by service category.

    Args:
        providers: List of provider dicts from Maps search
        category: Service category to filter by

    Returns:
        Filtered list of providers
    """
    return [p for p in providers if category.lower() in p.get("category", "").lower()]


def fetch_provider_availability(provider_id: str) -> List[dict]:
    """
    Fetch available time slots for a provider.

    Args:
        provider_id: Provider's unique ID

    Returns:
        List of available slot dicts
    """
    return MOCK_AVAILABILITY.get(provider_id, [])


def get_missing_fields(intent: dict) -> List[str]:
    """
    Identify which intent fields are missing.

    Args:
        intent: Partial intent dict

    Returns:
        List of missing field names
    """
    missing = []
    if not intent.get("location"):
        missing.append("location")
    if intent.get("service_type") == "Other":
        missing.append("service_type")
    if not intent.get("timing"):
        missing.append("timing")
    return missing


def format_clarification_question(missing_field: str, language: str = "hinglish") -> str:
    """
    Format a natural language clarification question.

    Args:
        missing_field: Field name that needs clarification
        language: 'urdu', 'english', or 'hinglish'

    Returns:
        Formatted question string
    """
    questions = {
        "location": {
            "hinglish": "Aap kahan hain? Area ya address bata dein.",
            "urdu": "آپ کہاں ہیں؟ علاقہ یا پتہ بتائیں۔",
            "english": "Could you share your location or area?",
        },
        "service_type": {
            "hinglish": "Kaunsa kaam chahiye? (e.g., Plumbing, AC, Bijli)",
            "urdu": "کون سا کام چاہیے؟",
            "english": "What type of service do you need?",
        },
        "timing": {
            "hinglish": "Kab chahiye? Aaj ya kal?",
            "urdu": "کب چاہیے؟",
            "english": "When would you like the service?",
        },
    }
    return questions.get(missing_field, {}).get(language, "Please provide more details.")


def send_availability_request(provider_id: str, slot_time: str) -> dict:
    """
    Send availability confirmation request to provider.

    Args:
        provider_id: Provider's unique ID
        slot_time: Requested time slot (ISO datetime string)

    Returns:
        dict with 'status': 'available'|'unavailable', 'message': str
    """
    # In production: call provider's registered endpoint / WhatsApp / SMS
    # Mock: always available for demo
    return {
        "status": "available",
        "provider_id": provider_id,
        "confirmed_slot": slot_time,
        "message": f"Provider {provider_id} confirmed for {slot_time}"
    }


def negotiate_timing(
    provider_id: str,
    preferred_time: str,
    alternative_slots: List[str]
) -> dict:
    """
    Negotiate alternative timing if preferred slot unavailable.

    Args:
        provider_id: Provider ID
        preferred_time: User's preferred time
        alternative_slots: List of provider's available slots

    Returns:
        dict with 'agreed_time' or 'no_agreement'
    """
    if alternative_slots:
        return {"agreed_time": alternative_slots[0], "negotiation_round": 1}
    return {"agreed_time": None, "negotiation_round": 2}


def get_provider_response(provider_id: str) -> dict:
    """
    Get latest response from provider's shadow agent.

    Args:
        provider_id: Provider ID

    Returns:
        dict with 'response_type', 'message', 'latency_ms'
    """
    return {
        "response_type": "acceptance",
        "message": "Job accepted",
        "latency_ms": 1200
    }
```

---

## `tools/elo_tools.py`

```python
from typing import Literal

def calculate_elo_score(
    current_elo: float,
    result: Literal["win", "loss"],
    opponent_elo: float = 1200.0,
    k_factor: float = 32.0
) -> float:
    """
    Update Elo score after a job outcome.

    Args:
        current_elo: Provider's current Elo score
        result: 'win' (job successful, ≥4 stars) or 'loss' (failed/≤2 stars)
        opponent_elo: Baseline Elo (default 1200 = average user expectation)
        k_factor: Sensitivity factor (lower for high-rated providers)

    Returns:
        New Elo score (float)
    """
    expected = 1 / (1 + 10 ** ((opponent_elo - current_elo) / 400))
    actual = 1.0 if result == "win" else 0.0
    return round(current_elo + k_factor * (actual - expected), 2)


def compute_proximity_score(distance_km: float, max_distance_km: float = 20.0) -> float:
    """
    Compute normalized proximity score (1.0 = closest, 0.0 = farthest).

    Args:
        distance_km: Provider's distance from user
        max_distance_km: Maximum search radius in km

    Returns:
        Proximity score between 0.0 and 1.0
    """
    score = 1.0 - (distance_km / max_distance_km)
    return max(0.0, min(1.0, score))


def compute_composite_score(
    elo_score: float,
    rating: float,
    distance_km: float,
    response_speed_ms: int,
    urgency_capable: bool,
    lifecycle_completion_rate: float,
    priority: str = "MEDIUM",
) -> dict:
    """
    Compute final weighted composite score for provider ranking.

    Args:
        elo_score: Raw Elo score
        rating: Verified rating (0–5)
        distance_km: Distance from user in km
        response_speed_ms: Shadow agent response latency
        urgency_capable: Whether provider handles emergencies
        lifecycle_completion_rate: Job completion rate (0–1)
        priority: User's intent priority (HIGH/MEDIUM/LOW)

    Returns:
        dict with 'composite_score' and 'breakdown'
    """
    # Normalize sub-scores to [0, 1]
    elo_norm = max(0.0, min(1.0, (elo_score - 800) / (2400 - 800)))
    rating_norm = rating / 5.0
    proximity = compute_proximity_score(distance_km)
    speed_norm = max(0.0, min(1.0, 1 - (response_speed_ms / 10000)))
    urgency_match = 1.0 if urgency_capable else (0.3 if priority == "HIGH" else 1.0)
    lifecycle_norm = lifecycle_completion_rate

    # Weighted sum
    composite = (
        0.35 * elo_norm +
        0.20 * rating_norm +
        0.20 * proximity +
        0.10 * speed_norm +
        0.10 * urgency_match +
        0.05 * lifecycle_norm
    )

    return {
        "composite_score": round(composite, 4),
        "breakdown": {
            "elo": round(elo_norm, 3),
            "rating": round(rating_norm, 3),
            "proximity": round(proximity, 3),
            "speed": round(speed_norm, 3),
            "urgency": round(urgency_match, 3),
            "lifecycle": round(lifecycle_norm, 3),
        }
    }
```

---

## `tools/booking_tools.py`

```python
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
```
