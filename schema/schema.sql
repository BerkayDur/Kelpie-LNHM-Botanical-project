USE plants; 
GO

DROP TABLE IF EXISTS alpha.FACT_plant_reading;
GO
DROP TABLE IF EXISTS alpha.DIM_plant;
GO
DROP TABLE IF EXISTS alpha.DIM_botanist;
GO

CREATE TABLE alpha.DIM_botanist (
    botanist_id INT IDENTITY(1, 1),
    name TEXT NOT NULL,
    email TEXT,
    phone_no TEXT,
    PRIMARY KEY (botanist_id)
);
GO
CREATE TABLE alpha.DIM_plant (
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
GO
CREATE TABLE alpha.FACT_plant_reading (
    reading_id INT IDENTITY(1, 1),
    soil_moisture FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    last_watered datetime2 NOT NULL CHECK(last_watered < CURRENT_TIMESTAMP),
    taken_at datetime2 NOT NULL,
    plant_id INT NOT NULL,
    botanist_id INT NOT NULL,
    PRIMARY KEY (reading_id),
    FOREIGN KEY (plant_id) REFERENCES alpha.DIM_plant(plant_id),
    FOREIGN KEY (botanist_id) REFERENCES alpha.DIM_botanist(botanist_id)
);
GO