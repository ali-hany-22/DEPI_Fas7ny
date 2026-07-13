CREATE SEQUENCE attraction_seq START 501;

CREATE TABLE attraction (
    attraction_id TEXT PRIMARY KEY DEFAULT
        ('AA' || nextval('attraction_seq')),
    attraction_name_en TEXT NOT NULL,
    attraction_name_ar TEXT NOT NULL,
    description_en TEXT NOT NULL,
    description_ar TEXT NOT NULL,
    
    category TEXT NOT NULL CHECK (category IN ('Historical', 'Cultural', 'Natural', 'Entertainment', 'Religious', 'Medical', 'Sports')),
    
    latitude NUMERIC(9, 6) CHECK (latitude >= -90 AND latitude <= 90),
    longitude NUMERIC(9, 6) CHECK (longitude >= -180 AND longitude <= 180),
    
    rating NUMERIC(2, 1) DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
    
    base_ticket_price NUMERIC(10, 2) DEFAULT 0 CHECK (base_ticket_price >= 0),

    city_id TEXT NOT NULL,
    CONSTRAINT fk_city
        FOREIGN KEY (city_id)
        REFERENCES city(city_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_attraction_city 
ON attraction(city_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE attraction_photo_seq START 501;
CREATE TABLE attraction_photo (
    attraction_photo_id TEXT PRIMARY KEY DEFAULT
        ('AAP' || nextval('attraction_photo_seq')),
    attraction_photo_url TEXT NOT NULL CHECK (
        attraction_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_attraction_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    attraction_id TEXT NOT NULL,
    CONSTRAINT fk_attraction
        FOREIGN KEY (attraction_id)
        REFERENCES attraction(attraction_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_attraction_photo_attraction
ON attraction_photo(attraction_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE attraction_activity_seq START 501;
CREATE TABLE attraction_activity (
    attraction_activity_id TEXT PRIMARY KEY DEFAULT
        ('AAA' || nextval('attraction_activity_seq')),
    activity_name_en TEXT NOT NULL,
    activity_name_ar TEXT NOT NULL,
    description_activity_en TEXT NOT NULL,
    description_activity_ar TEXT NOT NULL,
    price NUMERIC(10, 2) DEFAULT 0 CHECK (price >= 0),
    attraction_id TEXT NOT NULL,
    CONSTRAINT fk_attraction
        FOREIGN KEY (attraction_id)
        REFERENCES attraction(attraction_id)
        ON DELETE CASCADE,

    -- (Data Integrity) => not duplicate activities for the same attraction
    CONSTRAINT unique_attraction_activity UNIQUE (attraction_id, activity_name_en)
);
CREATE INDEX idx_attraction_activity_attraction
ON attraction_activity(attraction_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------
CREATE SEQUENCE attraction_activity_photo_seq START 501;
CREATE TABLE attraction_activity_photo (
    attraction_activity_photo_id TEXT PRIMARY KEY DEFAULT
        ('AAAP' || nextval('attraction_activity_photo_seq')),
    attraction_activity_photo_url TEXT NOT NULL CHECK (
        attraction_activity_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_attraction_activity_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    attraction_activity_id TEXT NOT NULL,
    CONSTRAINT fk_attraction_activity
        FOREIGN KEY (attraction_activity_id)
        REFERENCES attraction_activity(attraction_activity_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_attraction_activity_photo_attraction_activity
ON attraction_activity_photo(attraction_activity_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE attraction_activity_detail_seq START 501;
CREATE TABLE attraction_activity_detail (
    attraction_activity_detail_id TEXT PRIMARY KEY DEFAULT
        ('AAAD' || nextval('attraction_activity_detail_seq')),
    detail_name_en TEXT NOT NULL,
    detail_name_ar TEXT NOT NULL,
    description_detail_en TEXT NOT NULL,
    description_detail_ar TEXT NOT NULL,
    best_time_to_visit TEXT NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    booking_url TEXT NOT NULL CHECK (
        booking_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    is_suitable_for_kids BOOLEAN NOT NULL DEFAULT false,

    attraction_activity_id TEXT NOT NULL,
    CONSTRAINT fk_attraction_activity
        FOREIGN KEY (attraction_activity_id)
        REFERENCES attraction_activity(attraction_activity_id)
        ON DELETE CASCADE,
    CONSTRAINT unique_attraction_activity_detail UNIQUE (attraction_activity_id, detail_name_en)
);
CREATE INDEX idx_attraction_activity_detail_attraction_activity
ON attraction_activity_detail(attraction_activity_id);
    
