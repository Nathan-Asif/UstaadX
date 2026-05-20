from typing import List, Optional
# Fixed import path to point to our newly created models
from app.schemas.home_services_models import ProviderRecord, AvailableSlot

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
