CREATE SEQUENCE session_seq START 1001;

CREATE TABLE user_sessions (
    session_id TEXT PRIMARY KEY DEFAULT ('S' || nextval('session_seq')),
    
    user_id TEXT NOT NULL,
    
    access_token TEXT NOT NULL UNIQUE,
    refresh_token TEXT UNIQUE,
    
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_session_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_session_user ON user_sessions(user_id);