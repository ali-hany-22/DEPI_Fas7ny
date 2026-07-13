CREATE SEQUENCE user_seq START 1001;

CREATE TABLE users (
    user_id TEXT PRIMARY KEY DEFAULT ('U' || nextval('user_seq')),
    
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    
    phone TEXT,
    
    role TEXT NOT NULL CHECK (role IN ('customer', 'provider')),
    
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);