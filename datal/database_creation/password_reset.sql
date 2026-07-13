CREATE SEQUENCE password_reset_seq START 1001;

CREATE TABLE password_reset (
    reset_id TEXT PRIMARY KEY DEFAULT ('PR' || nextval('password_reset_seq')),
    
    user_id TEXT NOT NULL,
    
    reset_token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    is_used BOOLEAN DEFAULT false,

    CONSTRAINT fk_reset_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_reset_user ON password_reset(user_id);