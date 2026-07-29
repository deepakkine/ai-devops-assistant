#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get upgrade -y

apt-get install -y \
    docker.io \
    docker-compose-v2 \
    nginx \
    git \
    curl \
    unzip \
    jq \
    awscli

systemctl enable docker
systemctl start docker

systemctl enable nginx
systemctl start nginx

usermod -aG docker ubuntu

mkdir -p /home/ubuntu/ai-devops-assistant
chown -R ubuntu:ubuntu /home/ubuntu/ai-devops-assistant

echo "User data completed successfully"