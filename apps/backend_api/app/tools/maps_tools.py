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
