# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Install git
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Clone the repository
ARG GITHUB_REPO_URL
RUN git clone ${GITHUB_REPO_URL} .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=run.py

# Expose the port the app runs on
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "run:app"]