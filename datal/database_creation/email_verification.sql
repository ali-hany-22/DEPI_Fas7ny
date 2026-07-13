CREATE SEQUENCE email_verification_seq START 1001;

CREATE TABLE email_verification (
    verification_id TEXT PRIMARY KEY DEFAULT ('EV' || nextval('email_verification_seq')),
    
    user_id TEXT NOT NULL,
    
    verification_token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    is_verified BOOLEAN DEFAULT false,

    CONSTRAINT fk_verification_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);