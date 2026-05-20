-- Enable UUID extension (usually enabled by default in Supabase, but good to ensure)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Customers Table
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    location JSONB, -- Storing lat/lng or address string
    phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Technicians Table
CREATE TABLE technicians (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    location JSONB,
    base_elo INTEGER DEFAULT 1200, -- Default Elo rating
    skills TEXT[], -- Array of strings for skills (e.g., '{"AC Repair", "Plumbing"}')
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Agents Table
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    agent_type VARCHAR(50) NOT NULL, -- e.g., 'RANKING', 'NEGOTIATION'
    is_active BOOLEAN DEFAULT true, -- So we can toggle it on/off
    config JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. AgentLog Table
CREATE TABLE agent_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    task_id UUID, -- Optional link to a specific task if needed later
    action VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL, -- e.g., 'SUCCESS', 'FAILED', 'PENDING'
    details JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. CustomerActivity Table
CREATE TABLE customer_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    technician_id UUID REFERENCES technicians(id) ON DELETE SET NULL,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    interaction_log JSONB DEFAULT '{}'::jsonb, -- Flexible JSON for the conversation sequence
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optional but Recommended: Create helpful indexes for faster queries
CREATE INDEX idx_technicians_base_elo ON technicians(base_elo DESC);
CREATE INDEX idx_customer_activity_customer_id ON customer_activity(customer_id);
CREATE INDEX idx_agent_logs_agent_id ON agent_logs(agent_id);
