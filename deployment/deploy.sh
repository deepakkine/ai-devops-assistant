#!/bin/bash
set -euxo pipefail

echo "======================================="
echo "Starting deployment: $(date)"
echo "======================================="

PROJECT_DIR="/home/ubuntu/ai-devops-assistant"
COMPOSE_FILE="deployment/docker-compose.yml"
ENV_FILE=".env"

AWS_REGION="ap-south-1"
AWS_ACCOUNT_ID="848504403730"

cd "$PROJECT_DIR"

echo "===== Disk usage before deployment ====="
df -h

echo "===== Ensuring Docker is running ====="

sudo systemctl start docker
sudo systemctl enable docker

until docker info >/dev/null 2>&1; do
    echo "Waiting for Docker daemon..."
    sleep 2
done

echo "Docker is ready."

echo "===== Logging into Amazon ECR ====="

aws ecr get-login-password --region "$AWS_REGION" | \
docker login \
    --username AWS \
    --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

echo "===== Stopping existing containers ====="

docker compose \
    --env-file "$ENV_FILE" \
    -f "$COMPOSE_FILE" \
    down --remove-orphans || true

echo "===== Cleaning Docker builder cache ====="

docker builder prune -f

echo "===== Pulling latest image ====="

docker compose \
    --env-file "$ENV_FILE" \
    -f "$COMPOSE_FILE" \
    pull

echo "===== Starting application ====="

docker compose \
    --env-file "$ENV_FILE" \
    -f "$COMPOSE_FILE" \
    up -d --remove-orphans

echo "===== Waiting for container to start ====="

timeout 180 bash -c '
until docker ps --format "{{.Names}}" | grep -qx "ai-devops-assistant"; do
    sleep 2
done
'

echo "Container started."

echo "===== Waiting for container health ====="

timeout 180 bash -c '
until [ "$(docker inspect --format "{{.State.Health.Status}}" ai-devops-assistant)" = "healthy" ]; do
    echo "Waiting for healthy status..."
    sleep 5
done
'

echo "Container is healthy."

echo "===== Running containers ====="

docker compose \
    --env-file "$ENV_FILE" \
    -f "$COMPOSE_FILE" \
    ps

echo "===== Docker containers ====="

docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

echo "===== Verifying backend ====="

curl --fail --silent --show-error http://localhost:8000/health

echo
echo "✓ Local backend health check passed."

if curl --fail --silent --show-error https://deepakkine.online/health >/dev/null; then
    echo "✓ Public endpoint is healthy."
else
    echo "⚠ Public endpoint not yet reachable (continuing)."
fi

echo "===== Final cleanup ====="

docker image prune -f
docker builder prune -f

echo "===== Disk usage after deployment ====="

df -h

echo "======================================="
echo "Deployment completed successfully!"
echo "Finished at: $(date)"
echo "======================================="