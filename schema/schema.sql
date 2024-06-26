USE plants; 
GO

DROP TABLE IF EXISTS alpha.FACT_plant_reading;
DROP TABLE IF EXISTS alpha.DIM_plant;
DROP TABLE IF EXISTS alpha.DIM_botanist;
GO

CREATE TABLE alpha.DIM_botanist (
    botanist_id INT IDENTITY(1, 1),
    name NVARCHAR(50),
    email TEXT,
    phone_no TEXT,
    PRIMARY KEY (botanist_id)
);
GO

CREATE TABLE alpha.DIM_plant (
    plant_id INT,
    plant_name NVARCHAR(50),
    scientific_name TEXT,
    origin_longitude DECIMAL(9,6),
    origin_latitude DECIMAL(8,6),
    origin_town NVARCHAR(50),
    origin_country_code TEXT,
    origin_region TEXT,
    PRIMARY KEY (plant_id)
);
GO

CREATE TABLE alpha.FACT_plant_reading (
    reading_id INT IDENTITY(1, 1),
    soil_moisture FLOAT,
    temperature FLOAT,
    last_watered datetime2 CHECK(last_watered < CURRENT_TIMESTAMP),
    taken_at datetime2,
    plant_id INT,
    botanist_id INT,
    PRIMARY KEY (reading_id),
    FOREIGN KEY (botanist_id) REFERENCES alpha.DIM_botanist(botanist_id)
);
GO

INSERT INTO alpha.DIM_plant
(plant_id, plant_name, scientific_name, origin_longitude, origin_latitude, origin_town, origin_country_code, origin_region)
VALUES
(0, 'Epipremnum Aureum', Null, -41.25528, -19.32556, 'Resplendor', 'BR', 'America'),
(1, 'Venus flytrap', Null, -118.03917, 33.95015, 'South Whittier', 'US', 'America'),
(2, 'Corpse flower', Null, 4.92235, 7.65649, 'Efon-Alaaye', 'NG', 'Africa'),
(3, 'Rafflesia arnoldii', Null, -41.25528, -19.32556, 'Resplendor', 'BR', 'America'),
(4, 'Black bat flower', Null, -89.10944, 13.70167, 'Ilopango', 'SV', 'America'),
(5, 'Pitcher plant', 'Sarracenia catesbaei', 84.13864, 22.88783, 'Jashpurnagar', 'IN', 'Asia'),
(6, 'Wollemi pine', 'Wollemia nobilis', -79.2663, 43.86682, 'Markham', 'CA', 'America'),
(7, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(8, 'Bird of paradise', 'Heliconia schiedeana "Fire and Ice"', -3.59625, 5.27247, 'Bonoua', 'CI', 'Africa'),
(9, 'Cactus', 'Pereskia grandifolia', 11.32903, 50.9803, 'Weimar', 'DE', 'Europe'),
(10, 'Dragon tree,', Null, 16.43915, 43.50891, 'Split', 'HR', 'Europe'),
(11, 'Asclepias Curassavica', 'Asclepias curassavica', -156.47432, 20.88953, 'Kahului', 'US', 'Pacific'),
(12, 'Brugmansia X Candida', Null, -94.74049, 32.5007, 'Longview', 'US', 'America'),
(13, 'Canna ‘Striata’', Null, 8.61839, 49.68369, 'Bensheim', 'DE', 'Europe'),
(14, 'Colocasia Esculenta', 'Colocasia esculenta', -82.32483, 29.65163, 'Gainesville', 'US', 'America'),
(15, 'Cuphea ‘David Verity’', Null, 9.37082, 36.08497, 'Siliana', 'TN', 'Africa'),
(16, 'Euphorbia Cotinifolia', 'Euphorbia cotinifolia', -73.89875, 40.93121, 'Yonkers', 'US', 'America'),
(17, 'Ipomoea Batatas', 'Ipomoea batatas', 109.05389, -7.51611, 'Wangon', 'ID', 'Asia'),
(18, 'Manihot Esculenta ‘Variegata’', Null, 13.10984, 51.30001, 'Oschatz', 'DE', 'Europe'),
(19, 'Musa Basjoo', 'Musa basjoo', 27.46153, -21.44236, 'Tonota', 'BW', 'Africa'),
(20, 'Salvia Splendens', 'Salvia splendens', 1.10687, 41.15612, 'Reus', 'ES', 'Europe'),
(21, 'Anthurium', 'Anthurium andraeanum', -51.50361, -29.2975, 'Carlos Barbosa', 'BR', 'America'),
(22, 'Bird of Paradise', 'Heliconia schiedeana "Fire and Ice"', 10.98461, 48.35693, 'Friedberg', 'DE', 'Europe'),
-- (22, 'Cordyline Fruticosa', 'Cordyline fruticosa', 13.29371, 52.53048, 'Charlottenburg-Nord', 'DE', 'Europe'),
(23, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(24, 'Ficus', 'Ficus carica', 144.09638, 43.82634, 'Motomachi', 'JP', 'Asia'),
(25, 'Palm Trees', Null, 34.3869, 11.8659, 'Ar Ruseris', 'SD', 'Africa'),
(26, 'Dieffenbachia Seguine', 'Dieffenbachia seguine', 4.62744, 36.06386, 'El Achir', 'DZ', 'Africa'),
(27, 'Spathiphyllum', 'Spathiphyllum (group)', 33.9162, 51.67822, 'Hlukhiv', 'UA', 'Europe'),
(28, 'Croton', 'Codiaeum variegatum', -69.96533, 43.91452, 'Brunswick', 'US', 'America'),
(29, 'Aloe Vera', 'Aloe vera', 136.13108, 34.75856, 'Ueno-ebisumachi', 'JP', 'Asia'),
(30, 'Ficus Elastica', 'Ficus elastica', 20.22625, 30.75545, 'Ajdabiya', 'LY', 'Africa'),
(31, 'Sansevieria Trifasciata', 'Sansevieria trifasciata', 113.82465, 23.29549, 'Licheng', 'CN', 'Asia'),
(32, 'Philodendron Hederaceum', 'Philodendron hederaceum', 10.5511, 52.47774, 'Gifhorn', 'DE', 'Europe'),
(33, 'Schefflera Arboricola', 'Schefflera arboricola', 78.23456, 28.92694, 'Bachhraon', 'IN', 'Asia'),
(34, 'Aglaonema Commutatum', 'Aglaonema commutatum', 1.10687, 41.15612, 'Reus', 'ES', 'Europe'),
(35, 'Monstera Deliciosa', 'Monstera deliciosa', -71.23106, -32.45242, 'La Ligua', 'CL', 'America'),
(36, 'Tacca Integrifolia', 'Tacca integrifolia', -82.90375, 32.54044, 'Dublin', 'US', 'America'),
(37, 'Psychopsis Papilio', Null, 74.4818, 30.21121, 'Malaut', 'IN', 'Asia'),
(38, 'Saintpaulia Ionantha', 'Saintpaulia ionantha', 39.25, -6.8, 'Magomeni', 'TZ', 'Africa'),
(39, 'Gaillardia', 'Gaillardia aestivalis', 139.07204, 36.24624, 'Fujioka', 'JP', 'Asia'),
(40, 'Amaryllis', 'Hippeastrum (group)', 4.8951, 44.92801, 'Valence', 'FR', 'Europe'),
(41, 'Caladium Bicolor', 'Caladium bicolor', 88.1453, 22.4711, 'Pujali', 'IN', 'Asia'),
(42, 'Chlorophytum Comosum', 'Chlorophytum comosum "Vittatum"', 24.71204, 41.57439, 'Smolyan', 'BG', 'Europe'),
(43, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(44, 'Araucaria Heterophylla', 'Araucaria heterophylla', -103.5687, 20.22816, 'Zacoalco de Torres', 'MX', 'America'),
(45, 'Begonia', 'Begonia "Art Hodes"', -118.03917, 33.95015, 'South Whittier', 'US', 'America'),
(46, 'Medinilla Magnifica', 'Medinilla magnifica', 34.4587, -13.7804, 'Salima', 'MW', 'Africa'),
(47, 'Calliandra Haematocephala', 'Calliandra haematocephala', 15.07041, 37.49223, 'Catania', 'IT', 'Europe'),
(48, 'Zamioculcas Zamiifolia', 'Zamioculcas zamiifolia', 121.3152, 14.14989, 'Calauan', 'PH', 'Asia'),
(49, 'Crassula Ovata', 'Crassula ovata', -94.91386, 17.94979, 'Acayucan', 'MX', 'America'),
(50, 'Epipremnum Aureum', 'Epipremnum aureum', -41.25528, -19.32556, 'Resplendor', 'BR', 'America');
GO

INSERT INTO alpha.DIM_botanist (name, email, phone_no)
VALUES
('Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
('Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
('Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');
GO

