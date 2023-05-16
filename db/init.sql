\connect webcad_db;

-- Create a user table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id VARCHAR(255) NOT NULL UNIQUE
);

-- Create a table to track user interaction
CREATE TABLE interactions (
  id SERIAL PRIMARY KEY,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id VARCHAR(255) NOT NULL UNIQUE
);

-- Create an admin table
CREATE TABLE admins (
  id SERIAL PRIMARY KEY,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  username VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL
);