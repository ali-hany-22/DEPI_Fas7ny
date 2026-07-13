CREATE SEQUENCE transportation_id_seq START 2001;
CREATE TABLE transportation (
    transportation_id TEXT PRIMARY KEY DEFAULT
        ('TT' || nextval('transportation_id_seq')),
    transportation_type_nmae_en TEXT NOT NULL,
    transportation_type_name_ar TEXT NOT NULL,
    category_transportation TEXT NOT NULL, -- (General, Public, Private, Rental)
    description_transportation_en TEXT NOT NULL,
    description_transportation_ar TEXT NOT NULL,

    -- FK --> city
    city_id TEXT NOT NULL,
    CONSTRAINT fk_city
        FOREIGN KEY (city_id)
        REFERENCES city(city_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_transportation_city
ON transportation(city_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE transportation_photo_seq START 2001;
CREATE TABLE transportation_photo (
    transportation_photo_id TEXT PRIMARY KEY DEFAULT
        ('TTP' || nextval('transportation_photo_seq')),
    transportation_photo_url TEXT NOT NULL CHECK (
        transportation_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_transportation_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    transportation_id TEXT NOT NULL,
    CONSTRAINT fk_transportation
        FOREIGN KEY (transportation_id)
        REFERENCES transportation(transportation_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_transportation_photo_transportation
ON transportation_photo(transportation_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE transportation_start_station_seq START 2001;
CREATE TABLE transportation_start_station (
    transportation_start_station_id TEXT PRIMARY KEY DEFAULT
        ('TTSS' || nextval('transportation_start_station_seq')),
    station_name_en TEXT NOT NULL,
    station_name_ar TEXT NOT NULL,
    latitude NUMERIC(9, 6) CHECK (latitude >= -90 AND latitude <= 90),
    longitude NUMERIC(9, 6) CHECK (longitude >= -180 AND longitude <= 180),
    transportation_id TEXT NOT NULL,
    CONSTRAINT fk_transportation
        FOREIGN KEY (transportation_id)
        REFERENCES transportation(transportation_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_transportation_start_station_transportation
ON transportation_start_station(transportation_id);

    -- -------------------------------------------------------------------
    -- -------------------------------------------------------------------

CREATE SEQUENCE transportation_end_station_seq START 2001;
CREATE TABLE transportation_end_station (
    transportation_end_station_id TEXT PRIMARY KEY DEFAULT
        ('TTES' || nextval('transportation_end_station_seq')),
    station_name_en TEXT NOT NULL,
    station_name_ar TEXT NOT NULL,
    latitude NUMERIC(9, 6) CHECK (latitude >= -90 AND latitude <= 90),
    longitude NUMERIC(9, 6) CHECK (longitude >= -180 AND
longitude <= 180),
    transportation_id TEXT NOT NULL,
    CONSTRAINT fk_transportation
        FOREIGN KEY (transportation_id)
        REFERENCES transportation(transportation_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_transportation_end_station_transportation
ON transportation_end_station(transportation_id);

    --------------------------------------------------------------------
    --------------------------------------------------------------------
CREATE SEQUENCE transportation_route_seq START 2001;
CREATE TABLE transportation_route (
    transportation_route_id TEXT PRIMARY KEY DEFAULT
        ('TTR' || nextval('transportation_route_seq')),
    route_name_en TEXT NOT NULL,
    route_name_ar TEXT NOT NULL,
    description_route_en TEXT NOT NULL,
    description_route_ar TEXT NOT NULL,
    latitude NUMERIC(9, 6) CHECK (latitude >= -90 AND latitude <= 90),
    longitude NUMERIC(9, 6) CHECK (longitude >= -180 AND longitude <= 180),
    transportation_id TEXT NOT NULL,
    CONSTRAINT fk_transportation
        FOREIGN KEY (transportation_id)
        REFERENCES transportation(transportation_id)
        ON DELETE CASCADE,
    CONSTRAINT unique_transportation_route UNIQUE (transportation_id, route_name_en)
);
CREATE INDEX idx_transportation_route_transportation
ON transportation_route(transportation_id);

    --------------------------------------------------------------------
    --------------------------------------------------------------------
create sequence transportation_schedule_seq start 2001;
create table transportation_schedule (
    transportation_schedule_id TEXT PRIMARY KEY DEFAULT
        ('TTS' || nextval('transportation_schedule_seq')),
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    days_of_operation TEXT NOT NULL, -- e.g. "Mon, Wed, Fri"
    transportation_id TEXT NOT NULL,
    constraint fk_transportation
        foreign key (transportation_id)
        references transportation(transportation_id)       
        on delete cascade
);
create index idx_transportation_schedule_transportation
on transportation_schedule(transportation_id);

    --------------------------------------------------------------------
    -------------------------------------------------------------------

create sequence transportation_service_seq start 2001;
create table transportation_service (
    transportation_service_id TEXT PRIMARY KEY DEFAULT
        ('TTSV' || nextval('transportation_service_seq')),
    service_name_en TEXT NOT NULL,
    service_name_ar TEXT NOT NULL,
    description_service_en TEXT NOT NULL,
    description_service_ar TEXT NOT NULL,
    operating_hours TEXT NOT NULL, -- e.g. "9am - 5pm"
    service_icon_url TEXT NOT NULL CHECK (
        service_icon_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    service_link_url TEXT NOT NULL CHECK (
        service_link_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),

    transportation_id TEXT NOT NULL,
    constraint fk_transportation
        foreign key (transportation_id)
        references transportation(transportation_id)
        on delete cascade,
    constraint unique_transportation_service UNIQUE (transportation_id, service_name_en)
);

create index idx_transportation_service_transportation
on transportation_service(transportation_id);

    --------------------------------------------------------------------
    -------------------------------------------------------------------

CREATE SEQUENCE transportation_payment_method_service_seq START 2001;
CREATE TABLE transportation_payment_method_service (
    transportation_payment_method_service_id TEXT PRIMARY KEY DEFAULT
        ('TTPMS' || nextval('transportation_payment_method_service_seq')),
    
    payment_method_name_en TEXT NOT NULL,
    payment_method_name_ar TEXT NOT NULL,
    description_payment_method_en TEXT NOT NULL,
    description_payment_method_ar TEXT NOT NULL,
    
    service_icon_url TEXT NOT NULL CHECK (
        service_icon_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),

    transportation_service_id TEXT NOT NULL,
    CONSTRAINT fk_transportation_service
        FOREIGN KEY (transportation_service_id)
        REFERENCES transportation_service(transportation_service_id)
        ON DELETE CASCADE,
    
    -- التصحيح: القيد يعتمد على الأعمدة الموجودة فعلياً في الجدول
    CONSTRAINT unique_payment_per_service UNIQUE (transportation_service_id, payment_method_name_en)
);

CREATE INDEX idx_transportation_payment_method_service_transportation_service
ON transportation_payment_method_service(transportation_service_id);
    --------------------------------------------------------------------
    -------------------------------------------------------------------
CREATE SEQUENCE transportation_car_rental_seq START 2001;
CREATE TABLE transportation_car_rental (
    transportation_car_rental_id TEXT PRIMARY KEY DEFAULT
        ('TCR' || nextval('transportation_car_rental_seq')),
    rental_company_name_en TEXT NOT NULL,
    rental_company_name_ar TEXT NOT NULL,
    description_rental_company_en TEXT NOT NULL,
    description_rental_company_ar TEXT NOT NULL,
    rental_company_icon_url TEXT NOT NULL CHECK (
        rental_company_icon_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    rental_company_website_url TEXT NOT NULL CHECK (
        rental_company_website_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    car_details TEXT NOT NULL,

    transportation_id TEXT NOT NULL,
    constraint fk_transportation
        foreign key (transportation_id)
        references transportation(transportation_id)
        on delete cascade,
    constraint unique_transportation_car_rental UNIQUE (transportation_id, rental_company_name_en)
);
CREATE INDEX idx_transportation_car_rental_transportation
ON transportation_car_rental(transportation_id);

    --------------------------------------------------------------------
    -------------------------------------------------------------------
CREATE SEQUENCE transportation_car_rental_photo_seq START 2001;
CREATE TABLE transportation_car_rental_photo (
    transportation_car_rental_photo_id TEXT PRIMARY KEY DEFAULT
        ('TCRP' || nextval('transportation_car_rental_photo_seq')),
    transportation_car_rental_photo_url TEXT NOT NULL CHECK (
        transportation_car_rental_photo_url ~* '^https?://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$'
    ),
    description_transportation_car_rental_photo TEXT NOT NULL,
    cover_or_not BOOLEAN NOT NULL DEFAULT false,
    transportation_car_rental_id TEXT NOT NULL,
    CONSTRAINT fk_transportation_car_rental
        FOREIGN KEY (transportation_car_rental_id)
        REFERENCES transportation_car_rental(transportation_car_rental_id)
        ON DELETE CASCADE
);
CREATE INDEX idx_transportation_car_rental_photo_transportation_car_rental
ON transportation_car_rental_photo(transportation_car_rental_id);


    --------------------------------------------------------------------
    -------------------------------------------------------------------
ALTER TABLE transportation
ADD COLUMN provider_id TEXT,
ADD COLUMN data_source TEXT NOT NULL DEFAULT 'system' CHECK (data_source IN ('system', 'provider'));

ALTER TABLE transportation
ADD CONSTRAINT fk_transportation_provider
FOREIGN KEY (provider_id)
REFERENCES service_provider(provider_id)
ON DELETE SET NULL;

CREATE INDEX idx_transportation_provider ON transportation(provider_id);