#!/bin/bash
docker compose -f docker-compose.test.yml up -d
echo "Menunggu MySQL test ready..."
sleep 5
pytest "$@"
