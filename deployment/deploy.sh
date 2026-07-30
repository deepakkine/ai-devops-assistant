#!/bin/bash
set -euxo pipefail

cd /home/ubuntu/ai-devops-assistant

AWS_REGION="ap-south-1"
AWS_ACCOUNT_ID="848504403730"

sudo systemctl start docker

aws ecr get-login-password --region "$AWS_REGION" | \
docker login \
  --username AWS \
  --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

docker compose pull

docker compose down || true

docker compose up -d --remove-orphans

echo "Waiting for container to become healthy..."

timeout 180 bash -c '
until [ "$(docker inspect --format="{{.State.Health.Status}}" ai-devops-assistant)" = "healthy" ]; do
    sleep 5
done
'

docker compose ps

docker image prune -af

echo "Deployment completed successfully."