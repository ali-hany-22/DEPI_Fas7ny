CREATE SEQUENCE provider_seq START 501;

CREATE TABLE service_provider (
    provider_id TEXT PRIMARY KEY DEFAULT ('SP' || nextval('provider_seq')),
    
    user_id TEXT UNIQUE NOT NULL,
    
    business_name TEXT NOT NULL,
    business_type TEXT NOT NULL CHECK (
        business_type IN ('hotel', 'restaurant', 'rental', 'transportation')
    ),
    
    description TEXT,
    website_url TEXT CHECK (
        website_url IS NULL OR 
        website_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    
    is_verified BOOLEAN DEFAULT false,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_provider_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_provider_user ON service_provider(user_id);