-- -----------------------------------------------------
-- 1. CREATE DATABASE
-- -----------------------------------------------------
CREATE DATABASE IF NOT EXISTS paris_airbnb_dw;
USE paris_airbnb_dw;

-- -----------------------------------------------------
-- 2. CREATE DIMENSION TABLES (STAR SCHEMA)
-- -----------------------------------------------------

-- DIMENSION: dim_date
-- The most important table for time-series analysis in Tableau.
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week TINYINT NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    month TINYINT NOT NULL,
    quarter TINYINT NOT NULL,
    year INT NOT NULL,
    is_post_regulation BOOLEAN NOT NULL,
    is_covid_period BOOLEAN NOT NULL,
    UNIQUE(full_date)
);

-- DIMENSION: dim_hosts
CREATE TABLE IF NOT EXISTS dim_hosts (
    host_id BIGINT PRIMARY KEY,
    host_since DATE,
    host_location VARCHAR(255),
    host_response_time VARCHAR(50),
    host_response_rate FLOAT,
    host_acceptance_rate FLOAT,
    host_is_superhost BOOLEAN,
    host_total_listings_count INT,
    host_has_profile_pic BOOLEAN,
    host_identity_verified BOOLEAN
);

-- DIMENSION: dim_listings
CREATE TABLE IF NOT EXISTS dim_listings (
    listing_id BIGINT PRIMARY KEY,
    host_id BIGINT NOT NULL,
    name TEXT,
    neighbourhood VARCHAR(255),
    city VARCHAR(255),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    property_type VARCHAR(255),
    room_type VARCHAR(255),
    analytical_room_type VARCHAR(50), -- Our key analysis column
    accommodates INT,
    bedrooms INT,
    price FLOAT,
    minimum_nights INT,
    maximum_nights INT,
    review_scores_rating INT,
    review_scores_value INT,
    instant_bookable BOOLEAN,
    CONSTRAINT fk_listing_host FOREIGN KEY (host_id) REFERENCES dim_hosts(host_id)
);

-- -----------------------------------------------------
-- 3. CREATE FACT TABLE (STAR SCHEMA)
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS fact_reviews (
    review_id BIGINT PRIMARY KEY,
    listing_id BIGINT NOT NULL,
    host_id BIGINT NOT NULL,
    reviewer_id BIGINT, -- Degenerate dimension
    date_key INT NOT NULL,
    -- We can add metrics here later, e.g., 'price_at_time_of_review'
    CONSTRAINT fk_review_listing FOREIGN KEY (listing_id) REFERENCES dim_listings(listing_id),
    CONSTRAINT fk_review_host FOREIGN KEY (host_id) REFERENCES dim_hosts(host_id),
    CONSTRAINT fk_review_date FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);