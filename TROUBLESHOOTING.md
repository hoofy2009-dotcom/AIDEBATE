# 🔧 故障排查手册

## 📋 快速诊断

遇到问题？按以下顺序检查：

1. ✅ 服务是否运行？ → `docker compose ps`
2. ✅ 端口是否开放？ → 检查防火墙/安全组
3. ✅ 日志有什么错误？ → `docker compose logs`
4. ✅ 配置是否正确？ → 检查 `.env.production`

---

## 🚨 常见问题

### 问题 1：无法访问网站

#### 症状
- 浏览器显示 "无法访问此网站"
- 连接超时

#### 排查步骤

**步骤 1：检查容器状态**
```bash
docker compose ps
```

应该看到 3 个容器都是 `Up` 状态：
```
NAME                STATUS
ai-debate-backend   Up
ai-debate-frontend  Up
ai-debate-nginx     Up
```

如果有容器是 `Exit` 或 `Restarting`，继续下一步。

**步骤 2：查看日志**
```bash
# 查看所有日志
docker compose logs

# 查看后端日志
docker compose logs backend

# 查看前端日志
docker compose logs frontend
```

**步骤 3：检查端口**
```bash
# 检查 80 端口是否被占用
sudo netstat -tulpn | grep :80

# 检查 8000 端口
sudo netstat -tulpn | grep :8000
```

**步骤 4：检查防火墙**
```bash
# Ubuntu
sudo ufw status

# 如果未开放 80 端口
sudo ufw allow 80/tcp
```

**步骤 5：检查云服务器安全组**
- 登录云服务商控制台
- 找到 "安全组" 或 "防火墙" 设置
- 确保开放了 80 端口

#### 解决方案

如果容器未运行：
```bash
docker compose down
docker compose up -d
```

如果端口被占用：
```bash
# 查找占用进程
sudo lsof -i :80

# 停止占用进程
sudo kill -9 <PID>
```

---

### 问题 2：API Keys 错误

#### 症状
- AI 回复显示 "API 错误"
- 日志显示 "Unauthorized" 或 "Invalid API Key"

#### 排查步骤

**步骤 1：检查环境变量**
```bash
# 查看配置文件
cat .env.production

# 进入容器检查
docker compose exec backend env | grep API_KEY
```

**步骤 2：验证 API Keys**

测试 DeepSeek：
```bash
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

测试 DashScope（Qwen）：
```bash
curl https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 解决方案

重新配置环境变量：
```bash
# 编辑配置
nano .env.production

# 重启服务
docker compose restart
```

---

### 问题 3：WebSocket 连接失败

#### 症状
- 浏览器控制台显示 "WebSocket connection failed"
- AI 无法回复

#### 排查步骤

**步骤 1：检查 Nginx 配置**
```bash
docker compose exec frontend cat /etc/nginx/nginx.conf | grep -A 10 "location /ws/"
```

应该包含：
```nginx
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

**步骤 2：检查后端 WebSocket**
```bash
# 查看后端日志
docker compose logs backend | grep -i websocket
```

**步骤 3：测试 WebSocket**

在浏览器控制台运行：
```javascript
const ws = new WebSocket('ws://你的服务器IP/ws/debate');
ws.onopen = () => console.log('Connected');
ws.onerror = (e) => console.error('Error:', e);
```

#### 解决方案

重启 Nginx：
```bash
docker compose restart frontend
```

---

### 问题 4：前端页面空白

#### 症状
- 访问网站显示空白页面
- 没有任何内容

#### 排查步骤

**步骤 1：检查浏览器控制台**
按 F12 打开开发者工具，查看 Console 和 Network 标签

**步骤 2：检查 Nginx 日志**
```bash
docker compose exec frontend cat /var/log/nginx/error.log
```

**步骤 3：检查前端构建**
```bash
# 进入前端容器
docker compose exec frontend ls -la /usr/share/nginx/html
```

应该看到 `index.html` 和 `assets` 目录

#### 解决方案

重新构建前端：
```bash
docker compose down
docker compose build --no-cache frontend
docker compose up -d
```

---

### 问题 5：内存不足

#### 症状
- 容器频繁重启
- 日志显示 "OOMKilled"
- 系统响应缓慢

#### 排查步骤

**步骤 1：查看内存使用**
```bash
# 查看系统内存
free -h

# 查看容器内存
docker stats
```

**步骤 2：查看日志**
```bash
dmesg | grep -i "out of memory"
```

#### 解决方案

**方案 1：添加 Swap**
```bash
# 创建 2GB swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 永久生效
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 验证
free -h
```

**方案 2：限制容器内存**

编辑 `docker-compose.yml`：
```yaml
services:
  backend:
    mem_limit: 512m
  frontend:
    mem_limit: 256m
```

**方案 3：升级服务器**
- 升级到 4GB 内存配置

---

### 问题 6：Docker 命令无权限

#### 症状
- 运行 docker 命令提示 "permission denied"
- 需要 sudo

#### 解决方案

```bash
# 添加用户到 docker 组
sudo usermod -aG docker $USER

# 重新登录
exit
# 重新 ssh 连接

# 验证
docker ps
```

---

### 问题 7：构建失败

#### 症状
- `docker compose build` 失败
- 显示依赖安装错误

#### 排查步骤

**步骤 1：检查网络**
```bash
ping google.com
ping pypi.org
```

**步骤 2：查看构建日志**
```bash
docker compose build --no-cache --progress=plain
```

#### 解决方案

**方案 1：使用国内镜像**

创建 `/etc/docker/daemon.json`：
```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
```

重启 Docker：
```bash
sudo systemctl restart docker
```

**方案 2：配置 pip 镜像**

编辑 `backend/Dockerfile`，添加：
```dockerfile
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

**方案 3：配置 npm 镜像**

编辑 `frontend/Dockerfile`，添加：
```dockerfile
RUN npm config set registry https://registry.npmmirror.com
RUN npm install
```

---

### 问题 8：SSL/HTTPS 配置

#### 症状
- 想要启用 HTTPS
- 配置证书后无法访问

#### 解决方案

**使用 Let's Encrypt 免费证书**

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 申请证书
sudo certbot --nginx -d yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

**手动配置证书**

编辑 `docker/nginx.conf`：
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/your-cert.crt;
    ssl_certificate_key /etc/ssl/private/your-key.key;

    # ... 其他配置
}
```

---

### 问题 9：域名解析错误

#### 症状
- 域名无法访问
- IP 可以访问

#### 排查步骤

**步骤 1：检查 DNS 解析**
```bash
nslookup yourdomain.com
ping yourdomain.com
```

**步骤 2：检查域名配置**
- 登录域名提供商
- 检查 A 记录是否正确指向服务器 IP
- 等待 DNS 生效（可能需要 10 分钟 - 24 小时）

#### 解决方案

配置正确的 A 记录：
```
类型: A
主机记录: @
记录值: 你的服务器IP
TTL: 600
```

---

### 问题 10：API 响应慢

#### 症状
- AI 回复等待时间很长
- 超时错误

#### 排查步骤

**步骤 1：检查网络延迟**
```bash
# 测试 DeepSeek
curl -w "@curl-format.txt" -o /dev/null -s https://api.deepseek.com/v1/models

# 测试 DashScope
curl -w "@curl-format.txt" -o /dev/null -s https://dashscope.aliyuncs.com
```

**步骤 2：查看后端日志**
```bash
docker compose logs backend | grep -i "timeout\|slow\|error"
```

#### 解决方案

**方案 1：增加超时时间**

编辑 `docker/nginx.conf`：
```nginx
proxy_read_timeout 300s;
proxy_connect_timeout 300s;
```

**方案 2：选择更快的 API 节点**
- 国内用户使用阿里云百炼（Qwen）
- 选择物理距离近的服务器

---

## 🔍 调试工具

### 1. 查看实时日志
```bash
# 所有服务
docker compose logs -f

# 特定服务
docker compose logs -f backend

# 最后 100 行
docker compose logs --tail=100
```

### 2. 进入容器调试
```bash
# 进入后端容器
docker compose exec backend bash

# 进入前端容器
docker compose exec frontend sh

# 测试 Python 环境
docker compose exec backend python -c "import requests; print(requests.__version__)"
```

### 3. 网络诊断
```bash
# 检查端口
sudo netstat -tulpn

# 检查连接
sudo ss -tulpn

# 测试连接
curl -I http://localhost
curl -I http://localhost:8000/health
```

### 4. 性能监控
```bash
# 实时资源监控
docker stats

# 系统资源
htop
vmstat 1
iostat 1
```

---

## 📝 日志分析

### 常见错误信息

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `Connection refused` | 服务未启动 | `docker compose up -d` |
| `Unauthorized` | API Key 错误 | 检查 `.env.production` |
| `Module not found` | 依赖未安装 | 重新构建镜像 |
| `Port already in use` | 端口被占用 | 停止占用进程 |
| `OOMKilled` | 内存不足 | 添加 swap 或升级服务器 |
| `Cannot connect to Docker` | Docker 未启动 | `sudo systemctl start docker` |
| `WebSocket closed` | 网络中断 | 检查网络连接 |
| `Timeout` | 请求超时 | 增加超时时间或检查网络 |

---

## 🆘 紧急恢复

### 完全重置

如果一切都不工作，完全重置：

```bash
# 停止所有容器
docker compose down

# 删除所有容器和卷
docker compose down -v

# 清理镜像
docker system prune -a

# 重新部署
./deploy.sh
```

### 回滚到备份

```bash
# 恢复配置
cp .env.production.backup .env.production

# 重启服务
docker compose restart
```

---

## 📞 获取帮助

### 1. 收集诊断信息

运行以下命令并保存输出：

```bash
# 创建诊断报告
cat > diagnostic.sh << 'EOF'
#!/bin/bash
echo "=== 系统信息 ==="
uname -a
free -h
df -h

echo "=== Docker 状态 ==="
docker --version
docker compose version
docker compose ps

echo "=== 容器日志 ==="
docker compose logs --tail=50

echo "=== 环境配置 ==="
cat .env.production | grep -v "KEY="

echo "=== 端口监听 ==="
sudo netstat -tulpn | grep -E ":(80|443|8000)"
EOF

chmod +x diagnostic.sh
./diagnostic.sh > diagnostic.txt
```

### 2. 联系支持

- 📧 Email: support@example.com
- 💬 GitHub Issues: https://github.com/yourusername/ai-debate/issues
- 📖 文档: `CLOUD_DEPLOYMENT.md`

---

## ✅ 检查清单

遇到问题时，逐项检查：

- [ ] 容器是否运行？ `docker compose ps`
- [ ] 端口是否开放？ `sudo ufw status`
- [ ] 日志有错误吗？ `docker compose logs`
- [ ] 配置是否正确？ `cat .env.production`
- [ ] API Keys 是否有效？ 测试 API
- [ ] 网络是否正常？ `ping api.deepseek.com`
- [ ] 内存是否足够？ `free -h`
- [ ] 磁盘是否足够？ `df -h`

---

**祝您顺利解决问题！🎉**

如果以上方法都无法解决，请查看详细文档或联系技术支持。
