#!/bin/bash

clear
echo "REFRESHIHNG DEV ENVIRONMENT"

echo "Tearing down..."
docker compose down -v

echo ""
echo "Rebuilding..."
docker compose up -d --build

echo ""
echo "Seeding test data and performing tests..."
docker compose exec backend pytest -v