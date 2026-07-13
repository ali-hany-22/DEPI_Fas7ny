-- ===================================================================
--  (city)
-- ===================================================================
CREATE SEQUENCE city_id_seq START 1001;

CREATE TABLE city (
    city_id TEXT PRIMARY KEY DEFAULT ('CO' || nextval('city_id_seq')),
    city_name_en TEXT NOT NULL,
    city_name_ar TEXT NOT NULL,
    city_region_province TEXT NOT NULL,
    local_time_zone TEXT NOT NULL,
    about_the_city TEXT NOT NULL,

    latitude NUMERIC(9,6) NOT NULL CHECK (latitude >= -90 AND latitude <= 90),
    longitude NUMERIC(9,6) NOT NULL CHECK (longitude >= -180 AND longitude <= 180),
    is_capital BOOLEAN NOT NULL DEFAULT false,

    time_recorded TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    country_code TEXT NOT NULL,
    CONSTRAINT fk_city_country
        FOREIGN KEY (country_code)
        REFERENCES country(country_code)
        ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION update_time_on_coords()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.time_recorded = CURRENT_TIMESTAMP;
    ELSIF TG_OP = 'UPDATE' AND (
        NEW.latitude IS DISTINCT FROM OLD.latitude OR
        NEW.longitude IS DISTINCT FROM OLD.longitude
    ) THEN
        NEW.time_recorded = CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER city_coords_time_trigger
BEFORE INSERT OR UPDATE ON city
FOR EACH ROW
EXECUTE FUNCTION update_time_on_coords();

CREATE INDEX idx_city_name_en ON city(city_name_en);
CREATE INDEX idx_city_name_ar ON city(city_name_ar);

CREATE INDEX idx_city_country ON city(country_code);

CREATE UNIQUE INDEX idx_one_capital_per_country
ON city(country_code)
WHERE is_capital = true;

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_city_name_en_trgm ON city USING gin (city_name_en gin_trgm_ops);
CREATE INDEX idx_city_name_ar_trgm ON city USING gin (city_name_ar gin_trgm_ops);


-- ===================================================================
-- (city_photo)
-- ===================================================================
CREATE SEQUENCE city_photo_seq START 1001;

CREATE TABLE city_photo (
    city_photo_id TEXT PRIMARY KEY DEFAULT
        ('COP' || nextval('city_photo_seq')),
    city_photo_url TEXT NOT NULL CHECK (
        city_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_city_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    -- FK --> city
    city_id TEXT NOT NULL,
    CONSTRAINT fk_photo_city
        FOREIGN KEY (city_id)
        REFERENCES city(city_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_city_photo_city
ON city_photo(city_id);

CREATE UNIQUE INDEX idx_one_cover_per_city
ON city_photo(city_id)
WHERE cover_or_not = true;


-- ===================================================================
-- (city_tourism_type)
-- ===================================================================
CREATE SEQUENCE city_tourism_type_seq START 1001;

CREATE TABLE city_tourism_type (
    city_tourism_type_id TEXT PRIMARY KEY DEFAULT
        ('COT' || nextval('city_tourism_type_seq')),
    tourism_type_name TEXT NOT NULL,
    description_tourism_type TEXT NOT NULL,
    -- FK --> city
    city_id TEXT NOT NULL,
    CONSTRAINT fk_tourism_type_city
        FOREIGN KEY (city_id)
        REFERENCES city(city_id)
        ON DELETE CASCADE,
    -- يمنع تكرار نفس نوع السياحة لنفس المدينة
    CONSTRAINT uq_city_tourism_type
        UNIQUE (city_id, tourism_type_name)
);

CREATE INDEX idx_city_tourism_type_city
ON city_tourism_type(city_id);


-- ===================================================================
-- (city_tourism_type_photo)
-- ===================================================================
CREATE SEQUENCE city_tourism_type_photo_seq START 1001;

CREATE TABLE city_tourism_type_photo (
    city_tourism_type_photo_id TEXT PRIMARY KEY DEFAULT
        ('COTP' || nextval('city_tourism_type_photo_seq')),
    city_tourism_type_photo_url TEXT NOT NULL CHECK (
        city_tourism_type_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_city_tourism_type_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    -- FK --> city_tourism_type
    city_tourism_type_id TEXT NOT NULL,
    CONSTRAINT fk_city_tourism_type_photo
        FOREIGN KEY (city_tourism_type_id)
        REFERENCES city_tourism_type(city_tourism_type_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_city_tourism_type_photo_city_tourism_type
ON city_tourism_type_photo(city_tourism_type_id);

CREATE UNIQUE INDEX idx_one_cover_per_city_tourism_type
ON city_tourism_type_photo(city_tourism_type_id)
WHERE cover_or_not = true;


-- ===================================================================
-- (city_service_category)
-- ===================================================================
CREATE SEQUENCE city_service_cat_seq START 1001;

CREATE TABLE city_service_category (
    category_id TEXT PRIMARY KEY DEFAULT ('CSC' || nextval('city_service_cat_seq')),
    category_name_en TEXT NOT NULL, -- (Hospital, Bank, Police, Pharmacy, Gas Station)
    category_name_ar TEXT NOT NULL,
    icon_url TEXT CHECK (
        icon_url IS NULL OR
        icon_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    )      
);


-- ===================================================================
-- (city_service)
-- ===================================================================
CREATE SEQUENCE city_service_seq START 1001;

CREATE TABLE city_service (
    service_id TEXT PRIMARY KEY DEFAULT ('CS' || nextval('city_service_seq')),
    service_name_en TEXT NOT NULL,
    service_name_ar TEXT NOT NULL,

    address_en TEXT NOT NULL,
    address_ar TEXT NOT NULL,

    latitude NUMERIC(9,6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude NUMERIC(9,6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),

    phone_number TEXT CHECK (phone_number ~ '^\+?[0-9\s-]{7,15}$'),
    is_open_24h BOOLEAN DEFAULT false,

    city_id TEXT NOT NULL,
    category_id TEXT NOT NULL,

    CONSTRAINT fk_service_city
        FOREIGN KEY (city_id) REFERENCES city(city_id) ON DELETE CASCADE,
    CONSTRAINT fk_service_category
        FOREIGN KEY (category_id) REFERENCES city_service_category(category_id) ON DELETE CASCADE
);

CREATE INDEX idx_city_service_city ON city_service(city_id);
CREATE INDEX idx_city_service_category ON city_service(category_id);