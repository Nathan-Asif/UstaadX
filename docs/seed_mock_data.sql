-- Seed Mock Data for UstaadX
-- Copy and run this in your Supabase SQL Editor

-- Clear existing data (Optional, uncomment if you want a clean slate)
-- TRUNCATE customer_activity, agent_logs, agents, technicians, customers CASCADE;

-- 1. Insert Mock Customers
INSERT INTO customers (id, name, location, phone) VALUES
('11111111-1111-1111-1111-111111111111', 'Ali Khan', '{"lat": 24.8607, "lng": 67.0011, "city": "Karachi", "address": "DHA Phase 5"}', '+923001234567'),
('22222222-2222-2222-2222-222222222222', 'Sara Ahmed', '{"lat": 31.5204, "lng": 74.3587, "city": "Lahore", "address": "Gulberg III"}', '+923331234567'),
('33333333-3333-3333-3333-333333333333', 'Usman Tariq', '{"lat": 33.6844, "lng": 73.0479, "city": "Islamabad", "address": "F-8 Markaz"}', '+923451234567');

-- 2. Insert Mock Technicians (with varied Elo and Skills)
INSERT INTO technicians (id, name, location, base_elo, skills, is_active) VALUES
('44444444-4444-4444-4444-444444444444', 'Ustaad Rashid', '{"lat": 24.8610, "lng": 67.0020, "city": "Karachi"}', 1450, '{"AC Repair", "Refrigerator Repair"}', true),
('55555555-5555-5555-5555-555555555555', 'Ustaad Bilal', '{"lat": 31.5210, "lng": 74.3590, "city": "Lahore"}', 1200, '{"Plumbing", "Geyser Repair"}', true),
('66666666-6666-6666-6666-666666666666', 'Ustaad Kamran', '{"lat": 33.6850, "lng": 73.0480, "city": "Islamabad"}', 1600, '{"Electrician", "UPS Repair", "Solar Setup"}', true),
('77777777-7777-7777-7777-777777777777', 'Ustaad Faizan', '{"lat": 24.8500, "lng": 67.0100, "city": "Karachi"}', 1100, '{"AC Repair"}', true);

-- 3. Insert Agents
INSERT INTO agents (id, name, agent_type, is_active, config) VALUES
('88888888-8888-8888-8888-888888888888', 'Ustaad-Elo Engine', 'RANKING', true, '{"model": "gemini-3.1-pro", "threshold": 0.7}'),
('99999999-9999-9999-9999-999999999999', 'Proxy Negotiator', 'NEGOTIATION', true, '{"max_retries": 3, "timeout_mins": 15}');

-- 4. Insert Agent Logs
INSERT INTO agent_logs (agent_id, action, status, details) VALUES
('88888888-8888-8888-8888-888888888888', 'Ranked available technicians for AC Repair in Karachi', 'SUCCESS', '{"top_match": "44444444-4444-4444-4444-444444444444", "expected_performance": 0.85}'),
('99999999-9999-9999-9999-999999999999', 'Negotiated time slot with Ustaad Rashid', 'SUCCESS', '{"agreed_time": "14:00 PKT", "urgency_met": true}');

-- 5. Insert Customer Activity (Interaction Logs)
INSERT INTO customer_activity (customer_id, technician_id, agent_id, interaction_log) VALUES
(
  '11111111-1111-1111-1111-111111111111', 
  '44444444-4444-4444-4444-444444444444', 
  '88888888-8888-8888-8888-888888888888', 
  '{
    "2026-05-17T10:00:00Z": {"customer": "I need a technician to fix my AC at address, it is not cooling at all and guests are arriving.", "agent": "Sure, I am ranking the best AC technicians near you based on your urgency."},
    "2026-05-17T10:02:00Z": {"agent": "I have found Ustaad Rashid. He has a high success rate for emergency AC repairs in your area. Negotiating time now..."},
    "2026-05-17T10:05:00Z": {"technician": "Hello, I can be there by 2 PM. Is that okay?", "customer": "Yes, please be on time."}
  }'::jsonb
);
