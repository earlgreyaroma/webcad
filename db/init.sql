\connect mydatabase;

-- Create a table called "users"
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL UNIQUE,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
