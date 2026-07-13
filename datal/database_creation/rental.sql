CREATE SEQUENCE rental_id_seq START 401;
CREATE TABLE rental (
    rental_id TEXT PRIMARY KEY DEFAULT
        ('RE' || nextval('rental_id_seq')),
    rental_name_en TEXT NOT NULL,
    rental_name_ar TEXT NOT NULL,
    rental_type TEXT NOT NULL, -- (Apartment, Villa, Chalet)
    latitude NUMERIC(9, 6) CHECK (latitude >= -90 AND latitude <= 90),
    longitude NUMERIC(9, 6) CHECK (longitude >= -180 AND longitude <= 180),
    
    overall_rating NUMERIC(2, 1) DEFAULT 0 CHECK (overall_rating >= 0 AND overall_rating <= 5),
    
    booking_url TEXT NOT NULL CHECK (
        booking_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),

    city_id TEXT NOT NULL,
    CONSTRAINT fk_city
        FOREIGN KEY (city_id)
        REFERENCES city(city_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_rental_city 
ON rental(city_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE rental_units_seq START 401;
CREATE TABLE rental_units (
    rental_unit_id TEXT PRIMARY KEY DEFAULT
        ('REU' || nextval('rental_units_seq')),
    unit_name_en TEXT NOT NULL,
    unit_name_ar TEXT NOT NULL,
    
    number_of_rooms INTEGER NOT NULL CHECK (number_of_rooms >= 1),
    number_of_bedrooms INTEGER NOT NULL CHECK (number_of_bedrooms >= 0),
    number_of_bathrooms INTEGER NOT NULL CHECK (number_of_bathrooms >= 0),
    maximum_persons INTEGER NOT NULL CHECK (maximum_persons >= 1),
    
    price_per_night NUMERIC(10, 2) NOT NULL CHECK (price_per_night >= 0),

    rental_id TEXT NOT NULL,
    CONSTRAINT fk_rental
        FOREIGN KEY (rental_id)
        REFERENCES rental(rental_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_rental_units_rental 
ON rental_units(rental_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE rental_unit_photo_seq START 401;
CREATE TABLE rental_unit_photo (
    rental_unit_photo_id TEXT PRIMARY KEY DEFAULT
        ('REUP' || nextval('rental_unit_photo_seq')),
    rental_unit_photo_url TEXT NOT NULL CHECK (
        rental_unit_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_rental_unit_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    rental_unit_id TEXT NOT NULL,
    CONSTRAINT fk_rental_unit
        FOREIGN KEY (rental_unit_id)
        REFERENCES rental_units(rental_unit_id)
        ON DELETE CASCADE
);
-- for faster searching of photos by rental unit use index on rental_unit_id in rental_unit_photo
CREATE INDEX idx_rental_unit_photo_rental_unit
ON rental_unit_photo(rental_unit_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------
CREATE SEQUENCE rental_service_seq START 401;
CREATE TABLE rental_service (
    rental_service_id TEXT PRIMARY KEY DEFAULT
        ('RES' || nextval('rental_service_seq')),
    service_name_en TEXT NOT NULL,
    service_name_ar TEXT NOT NULL,
    
    description_service_en TEXT NOT NULL,
    description_service_ar TEXT NOT NULL,

    icon_url TEXT NOT NULL CHECK (
        icon_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),

    category_service TEXT NOT NULL, -- (General, Room, Bathroom, Kitchen, Entertainment, Outdoor)

    rental_id TEXT NOT NULL,
    CONSTRAINT fk_rental
        FOREIGN KEY (rental_id)
        REFERENCES rental(rental_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_rental_service_rental
ON rental_service(rental_id);


    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

ALTER TABLE rental
ADD COLUMN provider_id TEXT,
ADD COLUMN data_source TEXT NOT NULL DEFAULT 'system' CHECK (data_source IN ('system', 'provider'));

ALTER TABLE rental
ADD CONSTRAINT fk_rental_provider
FOREIGN KEY (provider_id)
REFERENCES service_provider(provider_id)
ON DELETE SET NULL;

CREATE INDEX idx_rental_provider ON rental(provider_id);