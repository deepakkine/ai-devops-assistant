#!/bin/bash
set -euxo pipefail

cd /home/ubuntu/ai-devops-assistant

AWS_REGION="ap-south-1"
AWS_ACCOUNT_ID="848504403730"

echo "===== Disk usage before deployment ====="
df -h

echo "===== Starting Docker ====="
sudo systemctl start docker

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

echo "===== Cleaning old Docker resources ====="
docker image prune -af
docker builder prune -af

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

echo "===== Final cleanup ====="
docker image prune -af

echo "===== Disk usage after deployment ====="
df -h

echo "===== Deployment completed successfully ====="