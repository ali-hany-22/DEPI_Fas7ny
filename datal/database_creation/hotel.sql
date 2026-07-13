CREATE SEQUENCE hotel_id_seq START 301;
CREATE TABLE hotel (
    hotel_id TEXT PRIMARY KEY DEFAULT
        ('HO' || nextval('hotel_id_seq')),
    hotel_name_en TEXT NOT NULL,
    hotel_name_ar TEXT NOT NULL,
    number_of_stars INTEGER NOT NULL CHECK (number_of_stars >= 1 AND number_of_stars <= 5),
    price_range TEXT NOT NULL CHECK (price_range IN ('$', '$$', '$$$', '$$$$')),
    address TEXT NOT NULL,
    latitude NUMERIC(9, 6) CHECK (latitude >= -90 AND latitude <= 90),
    longitude NUMERIC(9, 6) CHECK (longitude >= -180 AND longitude <= 180),
    away_from_city_center_km NUMERIC(5, 2) CHECK (away_from_city_center_km >= 0),
    city_id TEXT NOT NULL,
    CONSTRAINT fk_city
        FOREIGN KEY (city_id)
        REFERENCES city(city_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_hotel_city
ON hotel(city_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE hotel_service_seq START 301;
CREATE TABLE hotel_service (
    hotel_service_id TEXT PRIMARY KEY DEFAULT 
        ('HOS' || nextval('hotel_service_seq')),
    
    service_name_en TEXT NOT NULL,
    service_name_ar TEXT NOT NULL,
    
    category TEXT NOT NULL CHECK (category IN ('room', 'amenity', 'activity')),
    
    service_icon_url TEXT NOT NULL CHECK (
        service_icon_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    
    service_description_en TEXT NOT NULL,
    service_description_ar TEXT NOT NULL,
    
    is_free BOOLEAN NOT NULL DEFAULT true,

    hotel_id TEXT NOT NULL,
    CONSTRAINT fk_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES hotel(hotel_id)
        ON DELETE CASCADE,

    -- (Data Integrity) => not duplicate services for the same hotel
    CONSTRAINT unique_hotel_service UNIQUE (hotel_id, service_name_en)
);

CREATE INDEX idx_hotel_service_hotel 
ON hotel_service(hotel_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE hotel_review_seq START 301;
CREATE TABLE hotel_review (
    hotel_review_id TEXT PRIMARY KEY DEFAULT 
        ('HOR' || nextval('hotel_review_seq')),
    
    overall_rating NUMERIC(2, 1) DEFAULT 0 CHECK (overall_rating >= 0 AND overall_rating <= 5),
    number_of_reviews INTEGER NOT NULL DEFAULT 0 CHECK (number_of_reviews >= 0),
    
    staff_rating NUMERIC(2, 1) DEFAULT 0 CHECK (staff_rating >= 0 AND staff_rating <= 5),
    cleanliness_rating NUMERIC(2, 1) DEFAULT 0 CHECK (cleanliness_rating >= 0 AND cleanliness_rating <= 5),
    comfort_rating NUMERIC(2, 1) DEFAULT 0 CHECK (comfort_rating >= 0 AND comfort_rating <= 5),
    location_rating NUMERIC(2, 1) DEFAULT 0 CHECK (location_rating >= 0 AND location_rating <= 5),
    value_for_money_rating NUMERIC(2, 1) DEFAULT 0 CHECK (value_for_money_rating >= 0 AND value_for_money_rating <= 5),

    hotel_id TEXT NOT NULL UNIQUE, 
    CONSTRAINT fk_hotel
        FOREIGN KEY (hotel_id)  
        REFERENCES hotel(hotel_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_hotel_review_hotel
ON hotel_review(hotel_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE hotel_photo_seq START 301;
CREATE TABLE hotel_photo (
    hotel_photo_id TEXT PRIMARY KEY DEFAULT
        ('HOP' || nextval('hotel_photo_seq')),
    hotel_photo_url TEXT NOT NULL CHECK (
        hotel_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_hotel_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    hotel_id TEXT NOT NULL,
    CONSTRAINT fk_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES hotel(hotel_id)
        ON DELETE CASCADE
);  
-- for faster searching of photos by hotel use index on hotel_id in hotel_photo
CREATE INDEX idx_hotel_photo_hotel
ON hotel_photo(hotel_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE hotel_price_seq START 301;
CREATE TABLE hotel_price (
    hotel_price_id TEXT PRIMARY KEY DEFAULT
        ('HOPR' || nextval('hotel_price_seq')),
    room_type TEXT NOT NULL,
    cancelation_policy TEXT NOT NULL,
    price_per_night NUMERIC(10, 2) NOT NULL CHECK (price_per_night >= 0),
    currency TEXT NOT NULL,
    hotel_id TEXT NOT NULL,
    CONSTRAINT fk_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES hotel(hotel_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_hotel_price_hotel
ON hotel_price(hotel_id);


    --------------------------------------------------------------------
    ---------------------------------------------------------------------
ALTER TABLE hotel
ADD COLUMN provider_id TEXT,
ADD COLUMN data_source TEXT NOT NULL DEFAULT 'system' CHECK (data_source IN ('system', 'provider'));

ALTER TABLE hotel
ADD CONSTRAINT fk_hotel_provider
FOREIGN KEY (provider_id)
REFERENCES service_provider(provider_id)
ON DELETE SET NULL;

CREATE INDEX idx_hotel_provider ON hotel(provider_id);