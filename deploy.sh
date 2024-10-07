#!/bin/bash

# Pull the latest changes from the repository
git pull origin main

# Build and start the Docker containers
docker-compose up --build -d

# Run database migrations
docker-compose exec web flask db upgrade

# Optional: Clear cache, restart services, etc.
# docker-compose restart web