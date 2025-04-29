CREATE TABLE IF NOT EXISTS apartment (
    id SERIAL PRIMARY KEY,
    price NUMERIC(14,2) NOT NULL,
    area FLOAT,
    flat_toilets VARCHAR(50),
    balcony VARCHAR(50),
    current_floors INTEGER,
    total_floors INTEGER,
    ceiling FLOAT,
    dorm VARCHAR(10),
    mortgage VARCHAR(10),
    year INTEGER,
    type_of_house VARCHAR(50),
    repair_status VARCHAR(50),
    distance_to_center FLOAT
    );