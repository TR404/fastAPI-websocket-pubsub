# Use the official Python Alpine image as the base image
FROM python:3.9-alpine

# Install timezone data and Redis
RUN apk --no-cache add tzdata redis

# Set the timezone
ENV TZ=Asia/Kolkata

# Start Redis server when the container starts
# Note: This is a basic configuration; for production, you might want to customize the Redis configuration
CMD ["redis-server", "--daemonize", "yes"]

# Create a working directory
WORKDIR /opt/app

# Copy the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies without caching
# We install dependencies before creating a user to ensure that pip has the necessary permissions
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# Create a user 'appuser' and switch to it
# This is done after installing dependencies to avoid permission issues
RUN adduser -D appuser

# Change ownership of the /opt/app directory to appuser
# And grant full access to appuser
RUN chown -R appuser:appuser /opt/app && chmod -R 755 /opt/app

# Now switch to the non-root user
USER appuser

# Copy the rest of your application code
COPY . .

# Expose port 8000 for FastAPI and 6379 for Redis
EXPOSE 8000 6379

# Define the command to run your application
# Note: This CMD will override the previous CMD for Redis server. See Option 2 for a better approach.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
