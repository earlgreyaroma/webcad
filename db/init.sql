\connect webcad_db;

-- Create a user table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  admin_check BOOLEAN DEFAULT false,
  username VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255)
);

-- Track OnShape API Data
CREATE TABLE api_keys (
  id SERIAL PRIMARY KEY,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER REFERENCES users(id) UNIQUE,
  access_key VARCHAR(255),
  secret_key VARCHAR(255)
);

-- Create a table to track user interaction
CREATE TABLE actions (
  id SERIAL PRIMARY KEY,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER REFERENCES users(id)
);
