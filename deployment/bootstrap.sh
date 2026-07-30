#!/bin/bash
set -euxo pipefail

echo "===== Updating system ====="
apt-get update
apt-get upgrade -y

echo "===== Installing packages ====="
apt-get install -y \
    git \
    curl \
    unzip \
    nginx \
    docker.io \
    docker-compose-v2

echo "===== Enable Docker ====="
systemctl enable docker
systemctl start docker

echo "===== Enable Nginx ====="
systemctl enable nginx
systemctl start nginx

echo "===== Install AWS CLI ====="
if ! command -v aws >/dev/null; then
    ARCH=$(uname -m)

    if [ "$ARCH" = "x86_64" ]; then
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
    else
        curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "/tmp/awscliv2.zip"
    fi

    cd /tmp
    unzip -q awscliv2.zip
    ./aws/install
fi

echo "===== Clone Repository ====="

APP_DIR="/home/ubuntu/ai-devops-assistant"

if [ ! -d "$APP_DIR/.git" ]; then
    rm -rf "$APP_DIR"

    git clone \
      https://github.com/deepakkine/ai-devops-assistant.git \
      "$APP_DIR"
fi

echo "===== Fix ownership ====="

chown -R ubuntu:ubuntu "$APP_DIR"

echo "===== Bootstrap Complete ====="