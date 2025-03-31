#!/bin/bash

set -e  # Exit on any error
clear

echo "Refreshing Dev Environment"
echo "-----------------------------"

echo "Tearing down containers and volumes..."
docker compose down -v

echo ""
echo "Rebuilding and starting containers..."
docker compose up -d --build

echo ""
echo "Waiting for containers to be healthy..."
echo ""
echo "Container Status:"
docker compose ps --format table

echo ""
echo "Running tests with verbose output..."
docker compose exec backend pytest -v --disable-warnings --maxfail=5

echo ""
echo "Test run complete!"
