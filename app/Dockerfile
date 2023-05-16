# Use the official Python image as the base image
FROM python:3.11.3

# Change the working directory
WORKDIR /app

# Install the necessary system dependencies
RUN apt-get update

# Create and activate the virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Update ensurepip module and install pip
RUN python3 -m pip install --no-cache-dir --upgrade pip

# Copy and install the project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Set Environment variable
ENV PORT=5000

# Expose port 5000
EXPOSE 5000

# Start the Flask application
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
