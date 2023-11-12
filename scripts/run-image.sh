#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR/../"

IMAGE_NAME="ai-engine-anpr"
IMAGE_TAG=$(cat "$DIR/../VERSION")
PORT=$(cat "$DIR/port.txt")

echo "Running image $IMAGE_NAME:$IMAGE_TAG"
docker run -p $PORT:$PORT "$IMAGE_NAME:$IMAGE_TAG" -dit 