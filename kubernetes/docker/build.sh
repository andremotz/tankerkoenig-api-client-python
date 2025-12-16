#!/bin/bash
# Build-Skript für das Docker-Image
# Führt den Build vom tankerkoenig-api-client-python Verzeichnis aus

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$CLIENT_DIR"

IMAGE_NAME="${IMAGE_NAME:-diesel-price-logger}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
FULL_IMAGE_NAME="${FULL_IMAGE_NAME:-${IMAGE_NAME}:${IMAGE_TAG}}"

echo "Building Docker image: $FULL_IMAGE_NAME"
echo "Build context: $CLIENT_DIR"

docker build \
    -f kubernetes/docker/Dockerfile \
    -t "$FULL_IMAGE_NAME" \
    .

echo "Build erfolgreich! Image: $FULL_IMAGE_NAME"
echo ""
echo "Zum Pushen:"
echo "  docker push $FULL_IMAGE_NAME"

