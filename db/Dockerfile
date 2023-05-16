# Use the official PostgreSQL image as the base image
FROM postgres:13

# Set environment variables
ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD mypassword
ENV POSTGRES_DB webcad_db

# Copy the SQL script to the Docker image
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# Run PostgreSQL
CMD ["postgres"]