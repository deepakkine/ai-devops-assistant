#!/bin/bash

set -e

git pull

docker compose pull

docker compose up -d

docker image prune -f