
CREATE SEQUENCE restaurant_id_seq START 201;
CREATE TABLE restaurant (
    restaurant_id TEXT PRIMARY KEY DEFAULT 
        ('R' || nextval('restaurant_id_seq')),

    restaurant_name_en TEXT NOT NULL,
    restaurant_name_ar TEXT NOT NULL,

    cuisine_type TEXT NOT NULL,
    price_range TEXT NOT NULL CHECK (price_range IN ('$', '$$', '$$$', '$$$$')),
    rating NUMERIC(2, 1) CHECK (rating >= 0 AND rating <= 5),
    halal BOOLEAN NOT NULL,
    latitude NUMERIC(9, 6) CHECK (latitude >= -90 AND latitude <= 90),
    longitude NUMERIC(9, 6) CHECK (longitude >= -180 AND longitude <= 180),
    
    city_id TEXT NOT NULL,
    CONSTRAINT fk_city
        FOREIGN KEY (city_id)
        REFERENCES city(city_id)
        ON DELETE CASCADE

);
CREATE INDEX idx_restaurant_city
ON restaurant(city_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE restaurant_phone_seq START 201;
CREATE TABLE restaurant_phone (
    restaurant_phone_id TEXT PRIMARY KEY DEFAULT
        ('RP' || nextval('restaurant_phone_seq')),
    phone_number TEXT NOT NULL CHECK (phone_number ~ '^\+?[0-9\s-]{7,15}$'),
    restaurant_id TEXT NOT NULL,
    CONSTRAINT fk_restaurant
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurant(restaurant_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_restaurant_phone_restaurant
ON restaurant_phone(restaurant_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE restaurant_photo_seq START 201;
CREATE TABLE restaurant_photo (
    restaurant_photo_id TEXT PRIMARY KEY DEFAULT
        ('RPH' || nextval('restaurant_photo_seq')),
    restaurant_photo_url TEXT NOT NULL CHECK (
        restaurant_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_restaurant_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    restaurant_id TEXT NOT NULL,
    CONSTRAINT fk_restaurant
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurant(restaurant_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_restaurant_photo_restaurant
ON restaurant_photo(restaurant_id);
    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE restaurant_operating_details_id_seq START 201;
CREATE TABLE restaurant_operating_details (
    operating_details_id TEXT PRIMARY KEY DEFAULT
        ('ROD' || nextval('restaurant_operating_details_id_seq')),
        is_reservation_available BOOLEAN NOT NULL,
        opening_time TIME NOT NULL,
        closing_time TIME NOT NULL,
        week_end_opening_time TIME NOT NULL,
        week_end_closing_time TIME NOT NULL,
        outdoor_seating BOOLEAN NOT NULL,
        wear_style TEXT NOT NULL CHECK (wear_style IN ('casual', 'formal', 'smart casual', 'business casual')),
        menu_url TEXT NOT NULL CHECK (
            menu_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
        ),
        restaurant_id TEXT NOT NULL,
        CONSTRAINT fk_restaurant
            FOREIGN KEY (restaurant_id)
            REFERENCES restaurant(restaurant_id)
            ON DELETE CASCADE
);
CREATE INDEX idx_operating_details_restaurant
ON restaurant_operating_details(restaurant_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE restaurant_menu_id_seq START 201;
CREATE TABLE restaurant_menu (
    restaurant_menu_id TEXT PRIMARY KEY DEFAULT
        ('RM' || nextval('restaurant_menu_id_seq')),
    dish_name TEXT NOT NULL,
    description_dish TEXT NOT NULL,
    price NUMERIC(10, 2) CHECK (price >= 0),
    restaurant_id TEXT NOT NULL,
    CONSTRAINT fk_restaurant
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurant(restaurant_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_restaurant_menu_restaurant
ON restaurant_menu(restaurant_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------
CREATE SEQUENCE restaurant_menu_photo_id_seq START 201;
CREATE TABLE restaurant_menu_photo (
    restaurant_menu_photo_id TEXT PRIMARY KEY DEFAULT
        ('RMP' || nextval('restaurant_menu_photo_id_seq')),
    restaurant_menu_photo_url TEXT NOT NULL CHECK (
        restaurant_menu_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_restaurant_menu_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    restaurant_menu_id TEXT NOT NULL,
    CONSTRAINT fk_restaurant_menu
        FOREIGN KEY (restaurant_menu_id)
        REFERENCES restaurant_menu(restaurant_menu_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_restaurant_menu_photo_restaurant_menu
ON restaurant_menu_photo(restaurant_menu_id);


    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------
ALTER TABLE restaurant
ADD COLUMN provider_id TEXT,
ADD COLUMN data_source TEXT NOT NULL DEFAULT 'system' CHECK (data_source IN ('system', 'provider'));

ALTER TABLE restaurant
ADD CONSTRAINT fk_restaurant_provider
FOREIGN KEY (provider_id)
REFERENCES service_provider(provider_id)
ON DELETE SET NULL;

CREATE INDEX idx_restaurant_provider ON restaurant(provider_id);