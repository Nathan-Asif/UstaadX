import os
import sys

# Add the backend_api directory to the python path so the 'app' module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../apps/backend_api')))

from supabase import create_client, Client
# pyrefly: ignore [missing-import]
from app.core.config import settings

# Hardcoded for the seeding script to avoid import errors from other app modules
SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_SERVICE_ROLE_KEY

supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def seed_data():
    print("Starting to seed data to Supabase programmatically...")

    # 1. Customers
    customers = [
        {"id": "11111111-1111-1111-1111-111111111111", "name": "Ali Khan", "location": {"lat": 24.8607, "lng": 67.0011, "city": "Karachi", "address": "DHA Phase 5"}, "phone": "+923001234567"},
        {"id": "22222222-2222-2222-2222-222222222222", "name": "Sara Ahmed", "location": {"lat": 31.5204, "lng": 74.3587, "city": "Lahore", "address": "Gulberg III"}, "phone": "+923331234567"},
        {"id": "33333333-3333-3333-3333-333333333333", "name": "Usman Tariq", "location": {"lat": 33.6844, "lng": 73.0479, "city": "Islamabad", "address": "F-8 Markaz"}, "phone": "+923451234567"}
    ]
    supabase_client.table("customers").upsert(customers).execute()
    print(f"Seeded {len(customers)} customers.")

    # 2. Technicians
    technicians = [
        {"id": "44444444-4444-4444-4444-444444444444", "name": "Ustaad Rashid", "location": {"lat": 24.8610, "lng": 67.0020, "city": "Karachi"}, "base_elo": 1450, "skills": ["AC Repair", "Refrigerator Repair"], "is_active": True},
        {"id": "55555555-5555-5555-5555-555555555555", "name": "Ustaad Bilal", "location": {"lat": 31.5210, "lng": 74.3590, "city": "Lahore"}, "base_elo": 1200, "skills": ["Plumbing", "Geyser Repair"], "is_active": True},
        {"id": "66666666-6666-6666-6666-666666666666", "name": "Ustaad Kamran", "location": {"lat": 33.6850, "lng": 73.0480, "city": "Islamabad"}, "base_elo": 1600, "skills": ["Electrician", "UPS Repair", "Solar Setup"], "is_active": True},
        {"id": "77777777-7777-7777-7777-777777777777", "name": "Ustaad Faizan", "location": {"lat": 24.8500, "lng": 67.0100, "city": "Karachi"}, "base_elo": 1100, "skills": ["AC Repair"], "is_active": True}
    ]
    supabase_client.table("technicians").upsert(technicians).execute()
    print(f"Seeded {len(technicians)} technicians.")

    # 3. Agents
    agents = [
        {"id": "88888888-8888-8888-8888-888888888888", "name": "Ustaad-Elo Engine", "agent_type": "RANKING", "is_active": True, "config": {"model": "gemini-3.1-pro", "threshold": 0.7}},
        {"id": "99999999-9999-9999-9999-999999999999", "name": "Proxy Negotiator", "agent_type": "NEGOTIATION", "is_active": True, "config": {"max_retries": 3, "timeout_mins": 15}}
    ]
    supabase_client.table("agents").upsert(agents).execute()
    print(f"Seeded {len(agents)} agents.")

    # 4. Agent Logs
    agent_logs = [
        {"agent_id": "88888888-8888-8888-8888-888888888888", "action": "Ranked available technicians for AC Repair in Karachi", "status": "SUCCESS", "details": {"top_match": "44444444-4444-4444-4444-444444444444", "expected_performance": 0.85}},
        {"agent_id": "99999999-9999-9999-9999-999999999999", "action": "Negotiated time slot with Ustaad Rashid", "status": "SUCCESS", "details": {"agreed_time": "14:00 PKT", "urgency_met": True}}
    ]
    supabase_client.table("agent_logs").insert(agent_logs).execute()
    print(f"Seeded {len(agent_logs)} agent logs.")

    # 5. Customer Activity
    customer_activities = [
        {
            "customer_id": "11111111-1111-1111-1111-111111111111",
            "technician_id": "44444444-4444-4444-4444-444444444444",
            "agent_id": "88888888-8888-8888-8888-888888888888",
            "interaction_log": {
                "2026-05-17T10:00:00Z": {"customer": "I need a technician to fix my AC at address, it is not cooling at all and guests are arriving.", "agent": "Sure, I am ranking the best AC technicians near you based on your urgency."},
                "2026-05-17T10:02:00Z": {"agent": "I have found Ustaad Rashid. He has a high success rate for emergency AC repairs in your area. Negotiating time now..."},
                "2026-05-17T10:05:00Z": {"technician": "Hello, I can be there by 2 PM. Is that okay?", "customer": "Yes, please be on time."}
            }
        }
    ]
    supabase_client.table("customer_activity").insert(customer_activities).execute()
    print(f"Seeded {len(customer_activities)} customer activities.")

    print("Seeding complete!")

if __name__ == "__main__":
    seed_data()
