#!/bin/bash
set -euxo pipefail

echo "======================================="
echo "Starting deployment: $(date)"
echo "======================================="

PROJECT_DIR="/home/ubuntu/ai-devops-assistant"
COMPOSE_FILE="deployment/docker-compose.yml"
ENV_FILE=".env"
CONTAINER_NAME="ai-devops-assistant"

: "${AWS_REGION:?AWS_REGION is required}"
: "${AWS_ACCOUNT_ID:?AWS_ACCOUNT_ID is required}"

cd "$PROJECT_DIR"

echo "===== Disk usage before deployment ====="
df -h

echo "===== Docker disk usage before cleanup ====="
docker system df || true

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

echo "✓ ECR login successful."

echo "===== Checking for existing container ====="

if docker ps -a --format "{{.Names}}" | grep -qx "$CONTAINER_NAME"; then
    echo "Existing container found."

    if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME")" = "true" ]; then
        echo "Stopping running container..."
        docker stop "$CONTAINER_NAME"
    fi

    echo "Removing old container..."
    docker rm -f "$CONTAINER_NAME"
else
    echo "No existing container found."
fi

echo "===== Removing orphan containers ====="
docker compose \
    --env-file "$ENV_FILE" \
    -f "$COMPOSE_FILE" \
    down --remove-orphans || true

echo "===== Cleaning old Docker resources ====="

docker image prune -af || true
docker builder prune -af || true
docker volume prune -f || true

echo "===== Docker disk usage after cleanup ====="
docker system df || true

echo "===== Pulling latest image ====="

docker compose \
    --env-file "$ENV_FILE" \
    -f "$COMPOSE_FILE" \
    pull

echo "===== Starting application ====="

docker compose \
    --env-file "$ENV_FILE" \
    -f "$COMPOSE_FILE" \
    up -d \
    --force-recreate \
    --remove-orphans

echo "===== Waiting for container to start ====="

timeout 180 bash -c "
until docker ps --format '{{.Names}}' | grep -qx '$CONTAINER_NAME'; do
    sleep 2
done
"

echo "✓ Container started."

echo "===== Waiting for healthy status ====="

timeout 180 bash -c "
while true; do
    STATUS=\$(docker inspect --format '{{.State.Status}}' $CONTAINER_NAME)

    if [ \"\$STATUS\" = \"exited\" ]; then
        echo 'Container exited unexpectedly.'
        docker logs $CONTAINER_NAME
        exit 1
    fi

    HEALTH=\$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $CONTAINER_NAME)

    if [ \"\$HEALTH\" = \"healthy\" ]; then
        exit 0
    fi

    echo \"Current health: \$HEALTH\"
    sleep 5
done
"

echo "✓ Container is healthy."

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

echo "===== Final Docker cleanup ====="

docker image prune -f || true
docker builder prune -f || true

echo "===== Docker disk usage after deployment ====="
docker system df || true

echo "===== Disk usage after deployment ====="
df -h

echo "======================================="
echo "Deployment completed successfully!"
echo "Finished at: $(date)"
echo "======================================="