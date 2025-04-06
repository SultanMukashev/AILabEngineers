CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    gpa FLOAT,
    email VARCHAR(100) UNIQUE
)