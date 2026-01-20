#!/bin/bash

# AI Debate Platform - 云部署脚本
# 支持：阿里云、腾讯云、AWS、Azure 等

set -e

echo "======================================"
echo "  AI Debate Platform Cloud Deployment"
echo "======================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Docker
echo -e "${YELLOW}[1/6] Checking Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed!${NC}"
    echo "Please install Docker first:"
    echo "  curl -fsSL https://get.docker.com | sh"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed!${NC}"
    echo "Please install Docker Compose first"
    exit 1
fi
echo -e "${GREEN}✓ Docker installed${NC}"

# 检查 .env 文件
echo -e "${YELLOW}[2/6] Checking configuration...${NC}"
if [ ! -f ".env.production" ]; then
    echo -e "${RED}Error: .env.production not found!${NC}"
    echo "Please create .env.production with your API keys"
    exit 1
fi

# 复制 .env 文件
cp .env.production .env
echo -e "${GREEN}✓ Configuration loaded${NC}"

# 停止旧容器
echo -e "${YELLOW}[3/6] Stopping old containers...${NC}"
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✓ Old containers stopped${NC}"

# 构建镜像
echo -e "${YELLOW}[4/6] Building Docker images...${NC}"
docker-compose build --no-cache
echo -e "${GREEN}✓ Images built${NC}"

# 启动服务
echo -e "${YELLOW}[5/6] Starting services...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Services started${NC}"

# 等待服务启动
echo -e "${YELLOW}[6/6] Waiting for services to be ready...${NC}"
sleep 5

# 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓ All services are running!${NC}"
else
    echo -e "${RED}✗ Some services failed to start${NC}"
    docker-compose logs
    exit 1
fi

# 获取服务器 IP
SERVER_IP=$(curl -s ifconfig.me || echo "your-server-ip")

echo ""
echo "======================================"
echo "  🎉 Deployment Complete!"
echo "======================================"
echo ""
echo "📍 Access your platform at:"
echo "   http://${SERVER_IP}"
echo ""
echo "🔧 Useful commands:"
echo "   View logs:    docker-compose logs -f"
echo "   Restart:      docker-compose restart"
echo "   Stop:         docker-compose down"
echo "   Update:       git pull && ./deploy.sh"
echo ""
echo "📱 For mobile access:"
echo "   Open http://${SERVER_IP} on your iPhone"
echo ""
echo "======================================"
