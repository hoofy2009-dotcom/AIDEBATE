# 🎯 快速参考卡片

## 📝 常用命令速查表

### Docker 管理

```bash
# 查看容器状态
docker compose ps

# 启动服务
docker compose up -d

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 重启特定服务
docker compose restart backend
docker compose restart frontend

# 查看日志
docker compose logs
docker compose logs -f              # 实时日志
docker compose logs --tail=50       # 最后50行
docker compose logs backend         # 特定服务

# 进入容器
docker compose exec backend bash
docker compose exec frontend sh

# 重新构建
docker compose build --no-cache
docker compose up -d --build

# 查看资源使用
docker stats

# 清理系统
docker system prune -f
```

---

## 🔍 诊断命令

```bash
# 检查端口
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :8000
sudo lsof -i :80

# 检查防火墙
sudo ufw status
sudo ufw allow 80/tcp

# 测试 API
curl -I http://localhost
curl -I http://localhost:8000/health

# 查看系统资源
free -h                 # 内存
df -h                   # 磁盘
htop                    # 资源监控
vmstat 1                # 系统统计

# 查看环境变量
docker compose exec backend env | grep API_KEY
cat .env.production

# 测试网络
ping api.deepseek.com
ping dashscope.aliyuncs.com
curl -I https://api.deepseek.com
```

---

## 📂 重要文件路径

```
项目根目录
├── .env.production          # 生产环境配置（API Keys）
├── docker-compose.yml       # Docker 编排配置
├── deploy.sh                # 一键部署脚本
│
├── backend/
│   ├── main.py             # 后端主程序
│   ├── llm_providers.py    # AI 提供商
│   ├── web_search.py       # 搜索功能
│   └── requirements.txt    # Python 依赖
│
├── frontend/
│   ├── src/App.tsx         # 前端主组件
│   └── src/config.ts       # 前端配置
│
└── docker/
    └── nginx.conf          # Nginx 配置
```

---

## 🔑 环境变量配置

`.env.production` 文件格式：

```env
# DeepSeek API
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# Qwen (DashScope) API
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# Doubao (Volcengine) API
VOLCENGINE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
DOUBAO_ENDPOINT_ID=ep-m-xxxxxxxxxxxx-xxxxx
```

---

## 🌐 API Keys 获取地址

| AI | 获取地址 | Key 格式 |
|-----|---------|----------|
| DeepSeek | https://platform.deepseek.com/ | `sk-...` |
| Qwen | https://bailian.console.aliyun.com/ | `sk-...` |
| Doubao | https://console.volcengine.com/ark | `xxxxx-xxxx` + `ep-...` |

---

## 🚨 常见错误代码

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Connection refused` | 服务未启动 | `docker compose up -d` |
| `Unauthorized` | API Key 错误 | 检查 `.env.production` |
| `Port 80 in use` | 端口被占用 | `sudo lsof -i :80` 查找并停止 |
| `OOMKilled` | 内存不足 | 添加 Swap 或升级服务器 |
| `Cannot connect` | Docker 未启动 | `sudo systemctl start docker` |
| `WebSocket closed` | 网络问题 | 检查 Nginx 配置 |

---

## 📊 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Frontend (Nginx) | 80 | Web 界面 |
| Frontend (HTTPS) | 443 | HTTPS 访问 |
| Backend | 8000 | API 服务（内部） |
| WebSocket | 80/ws | 实时通信 |

---

## 🔧 快速修复

### 服务无法启动
```bash
docker compose down
docker compose up -d
```

### 完全重置
```bash
docker compose down -v
docker system prune -a
./deploy.sh
```

### 更新代码
```bash
git pull
docker compose down
docker compose build --no-cache
docker compose up -d
```

### 修改配置后重启
```bash
nano .env.production
docker compose restart
```

### 查看实时日志
```bash
docker compose logs -f backend
```

---

## 📱 移动端访问

### 本地网络
```bash
cd backend
python get_mobile_url.py
```
扫描二维码访问

### 云端访问
```
http://服务器IP
https://yourdomain.com
```

### 添加到主屏幕
Safari → 分享 → 添加到主屏幕

---

## 🔐 安全检查

```bash
# 修改 SSH 端口
sudo vim /etc/ssh/sshd_config

# 禁用 root 登录
# PermitRootLogin no

# 配置防火墙
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 定期更新
sudo apt update && sudo apt upgrade -y

# 查看登录历史
last
lastb
```

---

## 📈 性能优化

```bash
# 添加 Swap (2GB)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Docker 清理
docker system prune -f
docker volume prune -f

# 日志轮转
docker compose logs > logs.txt
truncate -s 0 $(docker inspect --format='{{.LogPath}}' ai-debate-backend-1)
```

---

## 🆘 紧急联系

| 问题类型 | 资源 |
|----------|------|
| 部署问题 | `QUICK_START.md` |
| 详细教程 | `CLOUD_DEPLOYMENT.md` |
| 故障排查 | `TROUBLESHOOTING.md` |
| 服务器选择 | `SERVER_RECOMMENDATION.md` |
| 部署清单 | `DEPLOYMENT_CHECKLIST.md` |

---

## ⚡ 一键命令

### 一键部署
```bash
curl -fsSL https://get.docker.com | sh && \
systemctl start docker && \
chmod +x deploy.sh && \
./deploy.sh
```

### 一键诊断
```bash
echo "=== Docker ===" && docker compose ps && \
echo "=== 端口 ===" && sudo netstat -tulpn | grep -E ":(80|8000)" && \
echo "=== 日志 ===" && docker compose logs --tail=20
```

### 一键重启
```bash
docker compose down && docker compose up -d && docker compose logs -f
```

---

## 📞 获取帮助

1. **查看文档**：`README.md`
2. **检查日志**：`docker compose logs`
3. **运行诊断**：`docker compose ps` + `docker stats`
4. **搜索错误**：复制错误信息到 Google
5. **提交问题**：GitHub Issues

---

**打印本页作为快速参考！📌**
