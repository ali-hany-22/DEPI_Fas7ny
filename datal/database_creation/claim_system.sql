CREATE SEQUENCE claim_seq START 1001;

CREATE TABLE service_claim_request (
    claim_id TEXT PRIMARY KEY DEFAULT ('CL' || nextval('claim_seq')),
    
    provider_id TEXT NOT NULL,
    
    service_type TEXT NOT NULL CHECK (
        service_type IN ('hotel', 'restaurant', 'rental', 'transportation')
    ),
    
    service_id TEXT NOT NULL, -- ID من الجدول الأساسي
    
    claim_status TEXT NOT NULL DEFAULT 'pending' CHECK (
        claim_status IN ('pending', 'approved', 'rejected')
    ),
    
    message TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_claim_provider
        FOREIGN KEY (provider_id)
        REFERENCES service_provider(provider_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_claim_provider ON service_claim_request(provider_id);
CREATE INDEX idx_claim_service ON service_claim_request(service_type, service_id);