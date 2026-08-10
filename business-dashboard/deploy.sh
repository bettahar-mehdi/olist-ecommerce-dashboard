#!/bin/bash
# ============================================================
# VPS Deployment Script for Olist E-Commerce Dashboard
# ============================================================
# Run this on a fresh Ubuntu/Debian VPS
# ============================================================

set -e

echo "=== Updating system ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing Docker ==="
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "=== Adding user to docker group ==="
sudo usermod -aG docker $USER

echo "=== Cloning dashboard repository ==="
read -p "Enter your GitHub repo URL: " REPO_URL
git clone $REPO_URL /home/$USER/dashboard
cd /home/$USER/dashboard

echo "=== Building and starting container ==="
docker build -t olist-dashboard .
docker run -d --name olist-dashboard --restart unless-stopped -p 8050:8050 olist-dashboard

echo "=== Deployment complete ==="
echo "Dashboard running at: http://$(curl -s ifconfig.me):8050"
echo ""
echo "Useful commands:"
echo "  docker logs -f olist-dashboard    # View logs"
echo "  docker restart olist-dashboard    # Restart"
echo "  docker stop olist-dashboard       # Stop"
