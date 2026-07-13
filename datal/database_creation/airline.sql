-- =========================================
-- AIRPORT
-- =========================================
CREATE TABLE airport (
    airport_code VARCHAR(3) PRIMARY KEY,
    airport_name VARCHAR NOT NULL,
    airport_type VARCHAR NOT NULL,

    latitude NUMERIC(9,6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude NUMERIC(9,6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),

    capacity INTEGER,
    number_of_runways SMALLINT,
    airport_hours VARCHAR,
    website TEXT CHECK (
        website IS NULL OR
        website ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),

    city_id TEXT NOT NULL,
    CONSTRAINT fk_airport_city
        FOREIGN KEY (city_id)
        REFERENCES city(city_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_airport_city 
ON airport(city_id);

-- =========================================
-- AIRPORT PHONE
-- =========================================
CREATE SEQUENCE airport_phone_seq START 3001;

CREATE TABLE airport_phone (
    airport_phone_id TEXT PRIMARY KEY DEFAULT
        ('AP' || nextval('airport_phone_seq')),
    phone_number TEXT NOT NULL CHECK (phone_number ~ '^\+?[0-9\s-]{7,15}$'),
    airport_code VARCHAR(3) NOT NULL,
    CONSTRAINT fk_airport_phone
        FOREIGN KEY (airport_code)
        REFERENCES airport(airport_code)
        ON DELETE CASCADE
);

CREATE INDEX idx_airport_phone_airport ON airport_phone(airport_code);

-- =========================================
-- AIRPORT PHOTO
-- =========================================
CREATE SEQUENCE airport_photo_seq START 3001;

CREATE TABLE airport_photo (
    airport_photo_id TEXT PRIMARY KEY DEFAULT
        ('APP' || nextval('airport_photo_seq')),
    airport_photo_url TEXT NOT NULL CHECK (
        airport_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_airport_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    airport_code VARCHAR(3) NOT NULL,
    CONSTRAINT fk_airport_photo
        FOREIGN KEY (airport_code)
        REFERENCES airport(airport_code)
        ON DELETE CASCADE
);

CREATE INDEX idx_airport_photo_airport 
ON airport_photo(airport_code);

CREATE UNIQUE INDEX idx_one_cover_per_airport
ON airport_photo(airport_code)
WHERE cover_or_not = true;

-- =========================================
-- AIRLINE
-- =========================================
CREATE TABLE airline (
    airline_id VARCHAR(10) PRIMARY KEY,

    name_english TEXT NOT NULL,
    name_arabic TEXT NOT NULL,

    type_of_airline TEXT CHECK (
        type_of_airline IN ('low cost', 'full service', 'cargo')
    ),

    country_code TEXT NOT NULL,
    airport_code VARCHAR(3) NOT NULL,

    CONSTRAINT fk_airline_country
        FOREIGN KEY (country_code)
        REFERENCES country(country_code)
        ON DELETE CASCADE,

    CONSTRAINT fk_airline_airport
        FOREIGN KEY (airport_code)
        REFERENCES airport(airport_code)
        ON DELETE CASCADE
);

CREATE INDEX idx_airline_airport 
ON airline(airport_code);

CREATE INDEX idx_airline_country
ON airline(country_code);

-- =========================================
-- FLIGHT ROUTE
-- =========================================
CREATE SEQUENCE flight_route_seq START 3001;

CREATE TABLE flight_route (
    route_number TEXT PRIMARY KEY DEFAULT
        ('FR' || nextval('flight_route_seq')),

    departure_airport_code VARCHAR(3) NOT NULL,
    arrival_airport_code VARCHAR(3) NOT NULL,

    CONSTRAINT fk_departure_airport
        FOREIGN KEY (departure_airport_code)
        REFERENCES airport(airport_code)
        ON DELETE CASCADE,

    CONSTRAINT fk_arrival_airport
        FOREIGN KEY (arrival_airport_code)
        REFERENCES airport(airport_code)
        ON DELETE CASCADE,

    -- منع مسار المطار لنفسه
    CONSTRAINT no_self_route
        CHECK (departure_airport_code <> arrival_airport_code),

    -- not duplicate routes in the same direction
    CONSTRAINT unique_route 
        UNIQUE (departure_airport_code, arrival_airport_code)
);

CREATE INDEX idx_departure_airport 
ON flight_route(departure_airport_code);
CREATE INDEX idx_arrival_airport 
ON flight_route(arrival_airport_code);

-- for faster searching of routes by departure and arrival airports
CREATE INDEX idx_route_search 
ON flight_route(departure_airport_code, arrival_airport_code);

-- =========================================
-- FLIGHT
-- =========================================
CREATE SEQUENCE flight_seq START 3001;

CREATE TABLE flight (
    flight_id TEXT PRIMARY KEY DEFAULT
        ('FL' || nextval('flight_seq')),

    route_number TEXT NOT NULL,
    airline_id VARCHAR(10) NOT NULL,

    expected_time INTERVAL,
    price NUMERIC(10,2) CHECK (price >= 0),

    CONSTRAINT fk_flight_route
        FOREIGN KEY (route_number)
        REFERENCES flight_route(route_number)
        ON DELETE CASCADE,

    CONSTRAINT fk_flight_airline
        FOREIGN KEY (airline_id)
        REFERENCES airline(airline_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_flight_route 
ON flight(route_number);
CREATE INDEX idx_flight_airline 
ON flight(airline_id);

CREATE INDEX idx_flight_composite 
ON flight(route_number, airline_id);

-- =========================================
-- FLIGHT SCHEDULE
-- =========================================
CREATE SEQUENCE flight_schedule_seq START 3001;

CREATE TABLE flight_schedule (
    flight_schedule_id TEXT PRIMARY KEY DEFAULT
        ('FS' || nextval('flight_schedule_seq')),

    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,

    flight_id TEXT NOT NULL,

    CONSTRAINT fk_schedule_flight
        FOREIGN KEY (flight_id)
        REFERENCES flight(flight_id)
        ON DELETE CASCADE

);

CREATE INDEX idx_schedule_flight 
ON flight_schedule(flight_id);

-- =========================================
-- FLIGHT DAYS
-- =========================================
CREATE TABLE flight_days (
    flight_id TEXT NOT NULL,

    day_of_week TEXT CHECK (
        day_of_week IN ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
    ),

    CONSTRAINT fk_days_flight
        FOREIGN KEY (flight_id)
        REFERENCES flight(flight_id)
        ON DELETE CASCADE,

    PRIMARY KEY (flight_id, day_of_week)
);