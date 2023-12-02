#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR"

export DEBIAN_FRONTEND=noninteractive

APP_PORT=$(cat "$DIR/port.txt")

# Run the app
cd "$DIR/../src"
uvicorn main:app --host 0.0.0.0 --port $APP_PORT