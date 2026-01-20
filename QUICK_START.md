# ⚡ 5分钟快速部署指南

## 🎯 目标
从零到部署完成，只需 5 分钟！

---

## 📝 准备工作（2分钟）

### 1️⃣ 购买云服务器
- **阿里云轻量服务器**：https://www.aliyun.com/product/swas
- 配置：**2核2G**，系统：**Ubuntu 22.04**
- 价格：¥30-60/月
- 记录：**服务器IP** 和 **root密码**

### 2️⃣ 开放端口
在服务器管理页面 → **防火墙/安全组** → 添加规则：
- **80** (HTTP)
- **443** (HTTPS)
- **22** (SSH)

### 3️⃣ 准备 API Keys
- DeepSeek: https://platform.deepseek.com/
- 阿里云百炼: https://bailian.console.aliyun.com/
- 火山引擎: https://console.volcengine.com/

---

## 🚀 部署步骤（3分钟）

### 第 1 步：连接服务器（30秒）

在 PowerShell 中运行：
```powershell
ssh root@8.222.242.128
# 输入密码
Hoofy2009

### 第 2 步：一键安装 Docker（60秒）

```bash
curl -fsSL https://get.docker.com | sh && systemctl start docker && systemctl enable docker
```

### 第 3 步：上传项目文件（30秒）

**选项 A：本地上传**

在本地 PowerShell 中运行：
```powershell
scp -r e:\项目\ai-debate root@你的服务器IP:/root/
```

**选项 B：Git 克隆**（如果有仓库）

在服务器上运行：
```bash
git clone https://github.com/hoofy2009-dotcom/AIDEBATE.git ai-debate
cd ai-debate
```

### 第 4 步：配置 API Keys（30秒）

```bash
cd ai-debate
nano .env.production
```

填入您的 Keys，然后保存（Ctrl+O, Enter, Ctrl+X）：
```env
DEEPSEEK_API_KEY=sk-2d3c3b815d454b51b75b963ea8398963
DASHSCOPE_API_KEY=sk-9b564f6d513c4777a9359f649e9943c2
VOLCENGINE_API_KEY=c0e03f57-af9f-4343-8273-c3663fe27395
DOUBAO_ENDPOINT_ID=ep-m-20260119234219-sqd59
```

### 第 5 步：一键部署（60秒）

```bash
chmod +x server-deploy.sh && ./server-deploy.sh
```

等待 1-2 分钟，看到 "✅ 部署成功！" 即可！

---

## ✅ 验证部署

### 1. 检查服务状态
```bash
docker compose ps
```

应该看到 3 个容器都是 `Up` 状态

### 2. 在浏览器访问
```
http://你的服务器IP
```

### 3. 在 iPhone 上访问
Safari 打开同样的地址！

---

## 🎉 完成！

现在您可以：
- ✅ 在电脑上使用
- ✅ 在 iPhone 上使用
- ✅ 关闭本地电脑，24/7 在线
- ✅ 随时随地访问

---

## 🔧 常用命令

```bash
# 查看日志
docker compose logs -f

# 重启服务
docker compose restart

# 停止服务
docker compose down

# 启动服务
docker compose up -d
```

---

## 🐛 遇到问题？

### 无法访问？
1. 检查服务器防火墙：`sudo ufw status`
2. 检查云服务商安全组是否开放 80 端口
3. 查看日志：`docker compose logs`

### API 报错？
检查 .env.production 是否正确配置

### 其他问题？
查看完整文档：`CLOUD_DEPLOYMENT.md`

---

## 📞 快速支持

- 查看详细文档：`CLOUD_DEPLOYMENT.md`
- 查看日志：`docker compose logs backend`
- 检查配置：`cat .env.production`

---

**恭喜！您已完成快速部署！🎉**
