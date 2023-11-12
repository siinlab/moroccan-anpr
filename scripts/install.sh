#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR"

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install ffmpeg libsm6 libxext6  -y

cd "$DIR/.."
pip install -r requirements.txt