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
