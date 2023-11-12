#!/bin/bash
set -e

DIR=$(dirname "$(realpath "$0")")
cd "$DIR"

export DEBIAN_FRONTEND=noninteractive

cd "$DIR/.."
pip install -r requirements.txt