CREATE TABLE service_ownership (
    ownership_id SERIAL PRIMARY KEY,
    
    provider_id TEXT NOT NULL,
    
    service_type TEXT NOT NULL,
    service_id TEXT NOT NULL,
    
    is_verified BOOLEAN DEFAULT false,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ownership_provider
        FOREIGN KEY (provider_id)
        REFERENCES service_provider(provider_id)
        ON DELETE CASCADE,

    CONSTRAINT unique_service_owner UNIQUE (service_type, service_id)
);