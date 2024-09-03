# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install Flask (and any other dependencies if necessary)
RUN pip install Flask

# Expose the port the Flask app runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "assignment1.py"]
