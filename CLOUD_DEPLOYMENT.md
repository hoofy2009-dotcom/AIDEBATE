# ☁️ 云部署完整指南

## 🎯 概述

本指南将帮助您将 AI 辩论平台部署到云服务器，实现：
- ✅ 24/7 在线访问
- ✅ 不依赖本地电脑
- ✅ iPhone 随时随地使用
- ✅ 专业稳定的服务

---

## 📋 前置要求

### 1. 云服务器
**推荐配置：**
- CPU: 2核心
- 内存: 2GB
- 硬盘: 20GB
- 带宽: 1Mbps+
- 系统: Ubuntu 20.04/22.04 或 CentOS 7/8

**推荐服务商：**
- 阿里云（国内）：https://www.aliyun.com/
- 腾讯云（国内）：https://cloud.tencent.com/
- AWS（国际）：https://aws.amazon.com/
- DigitalOcean（国际）：https://www.digitalocean.com/

**价格参考：**
- 阿里云轻量服务器：¥30-60/月
- 腾讯云轻量服务器：¥30-60/月
- DigitalOcean：$6-12/月

### 2. 域名（可选）
- 推荐购买域名（如 ai-debate.com）
- 或使用服务器 IP 地址访问

---

## 🚀 快速部署（推荐）

### 步骤 1：购买云服务器

以阿里云为例：

1. **注册账号**
   - 访问 https://www.aliyun.com/
   - 注册并完成实名认证

2. **购买服务器**
   - 选择"轻量应用服务器"
   - 配置：2核2G，带宽1M
   - 系统镜像：Ubuntu 22.04
   - 地域：选择离您最近的（如华东-上海）

3. **配置安全组**
   - 开放端口：80（HTTP）、443（HTTPS）、22（SSH）
   - 在服务器管理页面 → 安全组 → 添加规则

4. **获取服务器信息**
   - 记录公网 IP 地址
   - 记录 root 密码（或配置 SSH 密钥）

### 步骤 2：连接到服务器

**Windows 用户（使用 PowerShell）：**
```powershell
ssh root@你的服务器IP
# 输入密码
```

**Mac/Linux 用户：**
```bash
ssh root@你的服务器IP
# 输入密码
```

### 步骤 3：安装 Docker

```bash
# 更新系统
apt update && apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 启动 Docker
systemctl start docker
systemctl enable docker

# 验证安装
docker --version
```

### 步骤 4：上传项目文件

**方法 A：使用 Git（推荐）**

```bash
# 安装 Git
apt install git -y

# 克隆项目（如果您有 Git 仓库）
git clone https://github.com/yourusername/ai-debate.git
cd ai-debate
```

**方法 B：手动上传**

使用 WinSCP 或 FileZilla 上传整个 `ai-debate` 文件夹到服务器

### 步骤 5：配置环境变量

```bash
cd ai-debate

# 编辑生产环境配置
nano .env.production
```

填入您的 API Keys：
```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxx
VOLCENGINE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
DOUBAO_ENDPOINT_ID=ep-xxxxxxxxxxxx
```

保存：按 `Ctrl+O`，回车，`Ctrl+X`

### 步骤 6：部署

```bash
# 赋予执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

等待 3-5 分钟，部署完成！

### 步骤 7：访问平台

在浏览器打开：
```
http://你的服务器IP
```

在 iPhone Safari 打开同样的地址即可！

---

## 🔧 详细部署步骤

### 1. 服务器准备

#### 1.1 更新系统
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

#### 1.2 安装必要工具
```bash
# Ubuntu/Debian
sudo apt install -y git curl wget vim

# CentOS/RHEL
sudo yum install -y git curl wget vim
```

### 2. 安装 Docker 和 Docker Compose

#### 2.1 安装 Docker
```bash
# 使用官方脚本
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 添加当前用户到 docker 组
sudo usermod -aG docker $USER

# 重新登录使其生效
exit
# 重新 ssh 登录
```

#### 2.2 验证 Docker
```bash
docker --version
docker compose version
```

### 3. 部署应用

#### 3.1 上传代码

**选项 A：Git**
```bash
cd ~
git clone https://github.com/yourusername/ai-debate.git
cd ai-debate
```

**选项 B：SCP 上传**
```powershell
# 在本地 PowerShell 运行
scp -r e:\项目\ai-debate root@服务器IP:/root/
```

#### 3.2 配置环境

```bash
cd ~/ai-debate

# 复制环境变量模板
cp backend/.env .env.production

# 编辑配置
vim .env.production
```

填入真实的 API Keys

#### 3.3 构建和启动

```bash
# 构建镜像
docker compose build

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f
```

### 4. 配置防火墙

```bash
# Ubuntu (ufw)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS (firewalld)
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --reload
```

---

## 🌐 配置域名（可选）

### 步骤 1：域名解析

在域名提供商（如阿里云万网）添加 A 记录：
```
类型: A
主机记录: @
记录值: 你的服务器IP
TTL: 600
```

### 步骤 2：配置 Nginx（HTTPS）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 申请 SSL 证书
sudo certbot --nginx -d yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

### 步骤 3：更新 Nginx 配置

编辑 `docker/nginx.conf`，添加 HTTPS 配置

---

## 📊 运维管理

### 查看日志
```bash
# 查看所有日志
docker compose logs

# 实时查看日志
docker compose logs -f

# 查看特定服务
docker compose logs backend
docker compose logs frontend
```

### 重启服务
```bash
# 重启所有服务
docker compose restart

# 重启特定服务
docker compose restart backend
```

### 更新应用
```bash
# 拉取最新代码
git pull

# 重新构建和部署
docker compose down
docker compose build --no-cache
docker compose up -d
```

### 备份数据
```bash
# 备份环境变量
cp .env.production .env.production.backup

# 备份日志
tar -czf logs-$(date +%Y%m%d).tar.gz logs/
```

### 监控资源使用
```bash
# 查看容器状态
docker compose ps

# 查看资源使用
docker stats

# 磁盘使用
df -h
```

---

## 🔒 安全建议

### 1. 修改 SSH 端口
```bash
sudo vim /etc/ssh/sshd_config
# 修改 Port 22 为其他端口
sudo systemctl restart sshd
```

### 2. 禁用 root 登录
```bash
# 创建新用户
sudo adduser deploy
sudo usermod -aG sudo deploy
sudo usermod -aG docker deploy

# 禁用 root SSH 登录
sudo vim /etc/ssh/sshd_config
# 设置 PermitRootLogin no
```

### 3. 配置防火墙
```bash
# 仅开放必要端口
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 4. 定期更新
```bash
# 设置自动安全更新
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

---

## 🐛 故障排查

### 问题 1：容器无法启动

```bash
# 查看详细日志
docker compose logs backend
docker compose logs frontend

# 检查端口占用
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :8000
```

### 问题 2：无法访问

1. 检查防火墙设置
2. 检查云服务器安全组
3. 检查 Nginx 配置
4. 查看容器状态：`docker compose ps`

### 问题 3：API Keys 错误

```bash
# 进入容器检查环境变量
docker compose exec backend env | grep API_KEY
```

### 问题 4：内存不足

```bash
# 添加 swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 📱 移动端访问

部署完成后，在 iPhone 上：

1. **打开 Safari**
2. **访问** `http://你的服务器IP` 或 `https://yourdomain.com`
3. **添加到主屏幕**（可选）
   - 点击分享按钮
   - 选择"添加到主屏幕"
   - 像原生 App 一样使用

---

## 💰 成本估算

### 基础方案（¥30-60/月）
- 阿里云轻量服务器 2核2G
- 1M 带宽
- 20GB 存储

### 进阶方案（¥100-200/月）
- 4核4G 服务器
- 5M 带宽
- 50GB 存储
- 备用服务器
- CDN 加速

---

## 🎯 下一步

部署完成后，您可以：

1. ✅ 配置域名和 HTTPS
2. ✅ 添加更多 AI 模型
3. ✅ 实现用户系统
4. ✅ 添加数据持久化
5. ✅ 配置 CDN 加速

---

## 📞 技术支持

如遇问题，请查看：
1. Docker 日志：`docker compose logs`
2. Nginx 日志：`docker compose exec frontend cat /var/log/nginx/error.log`
3. 系统日志：`journalctl -u docker`

---

## ✅ 检查清单

部署前确认：
- [ ] 云服务器已购买
- [ ] SSH 可以连接
- [ ] 安全组已配置
- [ ] Docker 已安装
- [ ] API Keys 已准备
- [ ] .env.production 已配置

部署后确认：
- [ ] 容器正常运行（`docker compose ps`）
- [ ] 网站可以访问
- [ ] WebSocket 连接正常
- [ ] AI 回复正常
- [ ] 移动端访问正常

---

🎉 **恭喜！您已完成云部署！**

现在可以在任何地方使用您的 AI 辩论平台了！
