USE db_name; 
GO

DROP TABLE IF EXISTS DIM_plant;
DROP TABLE IF EXISTS DIM_botanist;
DROP TABLE IF EXISTS FACT_plant_reading;
GO

CREATE TABLE schema_name.DIM_botanist (
    botanist_id INT IDENTITY(1, 1),
    name TEXT NOT NULL,
    email TEXT,
    phone_no TEXT,
    PRIMARY KEY (botanist_id)
);

CREATE TABLE schema_name.DIM_plant (
    plant_id INT IDENTITY(1, 1),
    plant_name TEXT NOT NULL,
    scientific_name TEXT,
    origin_longitude DECIMAL(9,6),
    origin_latitude DECIMAL(8,6),
    origin_town TEXT,
    origin_country_code TEXT,
    origin_region TEXT,
    PRIMARY KEY (plant_id)
);

CREATE TABLE schema_name.FACT_plant_reading (
    reading_id INT IDENTITY(1, 1),
    soil_moisture FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    last_watered datetime2 NOT NULL CHECK(last_watered) < CURRENT_TIMESTAMP,
    taken_at datetime2 NOT NULL,
    plant_id INT NOT NULL,
    botanist_id INT NOT NULL,
    PRIMARY KEY (reading_id)
    FOREIGN KEY (plant_id) REFERENCES DIM_plant(plant_id)
    FOREIGN KEY (botanist_id) REFERENCES DIM_botanist(botanist_id)
);
GO