-- Promotion Hub Database Initialization
-- This script runs when the PostgreSQL container starts for the first time

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS promotion_hub;

-- Set search path
SET search_path TO promotion_hub;

-- Create tables
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'published',
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    engagement INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    username VARCHAR(100),
    profile_url VARCHAR(500),
    bio TEXT,
    score DECIMAL(3,2),
    decision VARCHAR(50),
    invited BOOLEAN DEFAULT FALSE,
    invited_at TIMESTAMP,
    responded BOOLEAN DEFAULT FALSE,
    responded_at TIMESTAMP,
    notes TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(platform, user_id)
);

CREATE TABLE IF NOT EXISTS actions (
    id SERIAL PRIMARY KEY,
    lead_id INTEGER REFERENCES leads(id),
    action_type VARCHAR(50) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    scheduled_at TIMESTAMP,
    executed_at TIMESTAMP,
    result TEXT,
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    module VARCHAR(100),
    function_name VARCHAR(100),
    line_number INTEGER,
    extra_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_leads_platform ON leads(platform);
CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score);
CREATE INDEX IF NOT EXISTS idx_leads_decision ON leads(decision);
CREATE INDEX IF NOT EXISTS idx_leads_invited ON leads(invited);
CREATE INDEX IF NOT EXISTS idx_actions_lead_id ON actions(lead_id);
CREATE INDEX IF NOT EXISTS idx_actions_status ON actions(status);
CREATE INDEX IF NOT EXISTS idx_actions_scheduled_at ON actions(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_logs_created_at ON logs(created_at);
CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level);
CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform);
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);

-- Insert some sample data for testing
INSERT INTO leads (platform, user_id, username, bio, score, decision)
VALUES
    ('telegram', 'test_user_1', 'testuser1', 'Business Intelligence Manager', 0.85, 'invite'),
    ('instagram', 'test_user_2', 'testuser2', 'Compliance Officer at Tech Corp', 0.72, 'save'),
    ('telegram', 'test_user_3', 'testuser3', 'VAT Specialist', 0.95, 'invite')
ON CONFLICT (platform, user_id) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA promotion_hub TO promotion_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA promotion_hub TO promotion_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA promotion_hub TO promotion_user;