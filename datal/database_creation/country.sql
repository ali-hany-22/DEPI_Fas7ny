-- ===================================================================
-- (country)
-- ===================================================================
CREATE TABLE country (
    country_code TEXT PRIMARY KEY,             
    country_name TEXT UNIQUE NOT NULL,
    phone_code TEXT NOT NULL,                  
    currency TEXT NOT NULL,
    official_language TEXT NOT NULL,
    continent TEXT NOT NULL CHECK (
        continent IN ('Africa','Asia','Europe','North America','South America','Australia','Antarctica')
    ),
    flag_url TEXT CHECK (
        flag_url IS NULL OR 
        flag_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    plug_type TEXT NOT NULL,
    climate_info TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

-- ===================================================================
-- (country_photo)
-- ===================================================================
CREATE SEQUENCE country_photo_seq START 101;

CREATE TABLE country_photo (
    country_photo_id TEXT PRIMARY KEY DEFAULT 
        ('CP' || nextval('country_photo_seq')),
    country_photo_url TEXT NOT NULL CHECK (
        country_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_country_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    -- FK --> country
    country_code TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT fk_photo_country
        FOREIGN KEY (country_code)
        REFERENCES country(country_code)
        ON DELETE CASCADE
);

CREATE INDEX idx_country_photo_country 
ON country_photo(country_code);

CREATE UNIQUE INDEX idx_one_cover_per_country
ON country_photo(country_code)
WHERE cover_or_not = true;

-- ===================================================================
-- (country_tourism_type)
-- ===================================================================
CREATE SEQUENCE country_tourism_type_seq START 101;

CREATE TABLE country_tourism_type (
    country_tourism_type_id TEXT PRIMARY KEY DEFAULT 
        ('CT' || nextval('country_tourism_type_seq')),
    tourism_type_name TEXT NOT NULL,
    description_tourism_type TEXT NOT NULL,
    -- FK --> country
    country_code TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT fk_tourism_type_country
        FOREIGN KEY (country_code)
        REFERENCES country(country_code)
        ON DELETE CASCADE,
    CONSTRAINT uq_country_tourism_type
        UNIQUE (country_code, tourism_type_name)
);

CREATE INDEX idx_country_tourism_type_country
ON country_tourism_type(country_code);

-- ===================================================================
-- (country_tourism_type_photo)
-- ===================================================================
CREATE SEQUENCE country_tourism_type_photo_seq START 101;

CREATE TABLE country_tourism_type_photo (
    country_tourism_type_photo_id TEXT PRIMARY KEY DEFAULT
        ('CTP' || nextval('country_tourism_type_photo_seq')),
    country_tourism_type_photo_url TEXT NOT NULL CHECK (
        country_tourism_type_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_country_tourism_type_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    -- FK --> country_tourism_type
    country_tourism_type_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT fk_tourism_type_photo
        FOREIGN KEY (country_tourism_type_id)
        REFERENCES country_tourism_type(country_tourism_type_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_country_tourism_type_photo_tourism_type 
ON country_tourism_type_photo(country_tourism_type_id);

CREATE UNIQUE INDEX idx_one_cover_per_tourism_type
ON country_tourism_type_photo(country_tourism_type_id)
WHERE cover_or_not = true;