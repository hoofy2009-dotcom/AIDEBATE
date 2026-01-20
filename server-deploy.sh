#!/bin/bash
# AI Debate 平台服务器端部署脚本

echo "================================"
echo "  AI 辩论平台一键部署脚本"
echo "================================"
echo ""

# 检查是否有 sudo 权限
SUDO=""
if [ "$EUID" -ne 0 ]; then 
   echo "⚠️  非 root 用户，使用 sudo 执行..."
   SUDO="sudo"
fi

echo "📦 步骤 1/5: 安装 Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | $SUDO sh
    $SUDO systemctl start docker
    $SUDO systemctl enable docker
    echo "✅ Docker 安装完成"
else
    echo "✅ Docker 已安装"
fi

echo ""
echo "📥 步骤 2/5: 克隆项目..."
cd ~
if [ -d "ai-debate" ]; then
    echo "⚠️  目录已存在，删除旧版本..."
    rm -rf ai-debate
fi

git clone https://github.com/hoofy2009-dotcom/AIDEBATE.git ai-debate
cd ai-debate

echo ""
echo "🔑 步骤 3/5: 配置 API Keys..."
cat > .env.production << 'EOF'
DEEPSEEK_API_KEY=sk-2d3c3b815d454b51b75b963ea8398963
DASHSCOPE_API_KEY=sk-9b564f6d513c4777a9359f649e9943c2
VOLCENGINE_API_KEY=c0e03f57-af9f-4343-8273-c3663fe27395
DOUBAO_ENDPOINT_ID=ep-m-20260119234219-sqd59
EOF
echo "✅ API Keys 已配置"

echo ""
echo "🐳 步骤 4/5: 构建 Docker 镜像..."
$SUDO docker compose build

echo ""
echo "🚀 步骤 5/5: 启动服务..."
$SUDO docker compose up -d

echo ""
echo "⏳ 等待服务启动..."
sleep 10

echo ""
echo "================================"
echo "  ✅ 部署完成！"
echo "================================"
echo ""
echo "📊 容器状态："
$SUDO docker compose ps

echo ""
echo "🌐 访问地址："
echo "   http://8.222.242.128"
echo ""
echo "📱 iPhone 访问："
echo "   在 Safari 打开同样的地址"
echo ""
echo "🔧 常用命令："
echo "   查看日志: docker compose logs -f"
echo "   重启服务: docker compose restart"
echo "   停止服务: docker compose down"
echo ""
