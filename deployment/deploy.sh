#!/bin/bash
set -euxo pipefail

echo "======================================="
echo "Starting deployment: $(date)"
echo "======================================="

cd /home/ubuntu/ai-devops-assistant

AWS_REGION="ap-south-1"
AWS_ACCOUNT_ID="848504403730"

echo "===== Disk usage before deployment ====="
df -h

echo "===== Ensuring Docker is running ====="

if ! systemctl is-active --quiet docker; then
    sudo systemctl start docker
fi

echo "===== Logging into Amazon ECR ====="

aws ecr get-login-password --region "$AWS_REGION" | \
docker login \
    --username AWS \
    --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

echo "===== Stopping existing containers ====="

docker compose \
    --env-file .env \
    -f deployment/docker-compose.yml \
    down --remove-orphans || true

echo "===== Cleaning Docker builder cache ====="

docker builder prune -f

echo "===== Pulling latest image ====="

docker compose \
    --env-file .env \
    -f deployment/docker-compose.yml \
    pull

echo "===== Starting application ====="

docker compose \
    --env-file .env \
    -f deployment/docker-compose.yml \
    up -d --remove-orphans

echo "===== Waiting for container to become healthy ====="

timeout 180 bash -c '
until docker inspect ai-devops-assistant >/dev/null 2>&1 &&
      [ "$(docker inspect --format="{{.State.Health.Status}}" ai-devops-assistant)" = "healthy" ]; do
    sleep 5
done
'

echo "===== Running containers ====="

docker compose \
    --env-file .env \
    -f deployment/docker-compose.yml \
    ps

echo "===== Running Docker containers ====="

docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"

echo "===== Verifying application ====="

curl --fail --silent http://localhost:8000/health

curl --fail --silent https://deepakkine.online/health || true

echo
echo "Application health check passed."

echo "===== Final cleanup ====="

docker image prune -af
docker builder prune -f

echo "===== Disk usage after deployment ====="

df -h

echo "======================================="
echo "Deployment completed successfully!"
echo "Finished at: $(date)"
echo "======================================="