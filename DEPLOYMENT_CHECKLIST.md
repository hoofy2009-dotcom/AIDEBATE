# ✅ 云部署检查清单

使用本清单确保每个步骤都正确完成。

---

## 📋 部署前准备

### 1. 云服务器购买
- [ ] 已购买云服务器（推荐：阿里云或腾讯云）
- [ ] 配置：至少 2核2G 内存
- [ ] 系统：Ubuntu 20.04/22.04 或 CentOS 7/8
- [ ] 已获取公网 IP 地址：`__________________`
- [ ] 已设置 root 密码或 SSH 密钥

### 2. 安全组/防火墙配置
- [ ] 已开放 **80** 端口（HTTP）
- [ ] 已开放 **443** 端口（HTTPS，如需要）
- [ ] 已开放 **22** 端口（SSH）
- [ ] 已在云服务商控制台配置安全组

### 3. API Keys 准备
- [ ] DeepSeek API Key：`sk-_______________`
  - 获取地址：https://platform.deepseek.com/
- [ ] DashScope API Key：`sk-_______________`
  - 获取地址：https://bailian.console.aliyun.com/
- [ ] Volcengine API Key：`_______________`
  - 获取地址：https://console.volcengine.com/ark
- [ ] Doubao Endpoint ID：`ep-_______________`

### 4. 本地准备
- [ ] 已安装 SSH 客户端
- [ ] 已安装文件传输工具（如 WinSCP、FileZilla）
- [ ] 项目文件已准备好上传

---

## 🚀 部署步骤

### 第 1 步：连接服务器
- [ ] 成功通过 SSH 连接到服务器
  ```powershell
  ssh root@你的服务器IP
  ```
- [ ] 可以执行命令

### 第 2 步：安装 Docker
- [ ] 运行安装命令：
  ```bash
  curl -fsSL https://get.docker.com | sh
  ```
- [ ] 启动 Docker：
  ```bash
  systemctl start docker
  systemctl enable docker
  ```
- [ ] 验证安装：
  ```bash
  docker --version
  docker compose version
  ```
- [ ] Docker 版本：`__________________`

### 第 3 步：上传项目文件
选择以下一种方式：

**选项 A：使用 Git**
- [ ] 安装 Git：`apt install git -y`
- [ ] 克隆项目：`git clone <仓库地址>`
- [ ] 进入目录：`cd ai-debate`

**选项 B：手动上传**
- [ ] 使用 SCP 上传项目文件夹
  ```powershell
  scp -r e:\项目\ai-debate root@服务器IP:/root/
  ```
- [ ] 在服务器上确认文件存在：`ls -la /root/ai-debate`

### 第 4 步：配置环境变量
- [ ] 进入项目目录：`cd /root/ai-debate`
- [ ] 创建生产环境配置：
  ```bash
  nano .env.production
  ```
- [ ] 填入 API Keys：
  ```env
  DEEPSEEK_API_KEY=sk-your-key-here
  DASHSCOPE_API_KEY=sk-your-key-here
  VOLCENGINE_API_KEY=your-key-here
  DOUBAO_ENDPOINT_ID=ep-your-endpoint-here
  ```
- [ ] 保存文件：Ctrl+O, Enter, Ctrl+X
- [ ] 验证配置：`cat .env.production`

### 第 5 步：运行部署脚本
- [ ] 赋予执行权限：
  ```bash
  chmod +x deploy.sh
  ```
- [ ] 运行部署：
  ```bash
  ./deploy.sh
  ```
- [ ] 等待构建完成（3-5 分钟）
- [ ] 看到 "✅ 部署成功！" 消息

### 第 6 步：验证部署
- [ ] 检查容器状态：
  ```bash
  docker compose ps
  ```
- [ ] 所有容器状态为 `Up`
- [ ] 查看日志无错误：
  ```bash
  docker compose logs --tail=50
  ```

---

## 🔍 验证测试

### 1. Web 访问测试
- [ ] 在电脑浏览器打开：`http://你的服务器IP`
- [ ] 页面正常加载，显示 AI 辩论界面
- [ ] 无控制台错误（F12 查看）

### 2. 功能测试
- [ ] 输入测试主题："人工智能的未来"
- [ ] 选择辩论轮数：2
- [ ] 选择总结 AI：DeepSeek
- [ ] 点击"开始辩论"
- [ ] 三个 AI 依次发言
- [ ] 显示当前轮次
- [ ] 辩论结束显示总结
- [ ] 总结以金色显示

### 3. 移动端测试
- [ ] 在 iPhone Safari 打开：`http://你的服务器IP`
- [ ] 页面自适应移动端
- [ ] 可以正常输入和点击
- [ ] AI 回复正常显示
- [ ] 滚动流畅，无卡顿

### 4. WebSocket 测试
- [ ] 打开浏览器开发者工具（F12）
- [ ] Network → WS 标签
- [ ] 看到 WebSocket 连接（绿色）
- [ ] 发起辩论时，WebSocket 有数据传输

---

## 🔧 可选配置

### 域名配置（推荐）
- [ ] 已购买域名：`__________________`
- [ ] 域名 A 记录指向服务器 IP
- [ ] DNS 解析生效（24小时内）
- [ ] 域名可以访问网站

### HTTPS 配置（推荐）
- [ ] 安装 Certbot：
  ```bash
  apt install certbot python3-certbot-nginx -y
  ```
- [ ] 申请证书：
  ```bash
  certbot --nginx -d yourdomain.com
  ```
- [ ] 证书申请成功
- [ ] HTTPS 访问正常

### 防火墙配置
- [ ] 启用防火墙：
  ```bash
  ufw enable
  ```
- [ ] 允许必要端口：
  ```bash
  ufw allow 22/tcp
  ufw allow 80/tcp
  ufw allow 443/tcp
  ```
- [ ] 验证规则：`ufw status`

### 系统优化
- [ ] 添加 Swap（如内存 < 4GB）：
  ```bash
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  echo '/swapfile none swap sw 0 0' >> /etc/fstab
  ```
- [ ] 验证：`free -h`

---

## 📊 运维检查

### 日常检查
- [ ] 容器运行状态：`docker compose ps`
- [ ] 日志无异常：`docker compose logs --tail=50`
- [ ] 系统资源正常：`free -h` 和 `df -h`
- [ ] 网站可访问

### 每周检查
- [ ] 系统更新：`apt update && apt upgrade`
- [ ] Docker 清理：`docker system prune -f`
- [ ] 备份配置：`cp .env.production .env.production.backup`
- [ ] 查看访问日志

### 每月检查
- [ ] SSL 证书有效期（如使用 HTTPS）
- [ ] 服务器续费状态
- [ ] 性能监控和优化
- [ ] 安全补丁更新

---

## 🐛 故障排查

遇到问题时，按顺序检查：

1. **无法访问**
   - [ ] 检查容器：`docker compose ps`
   - [ ] 检查日志：`docker compose logs`
   - [ ] 检查端口：`netstat -tulpn | grep 80`
   - [ ] 检查防火墙：`ufw status`
   - [ ] 检查安全组

2. **API 错误**
   - [ ] 验证 API Keys
   - [ ] 检查环境变量：`docker compose exec backend env | grep API_KEY`
   - [ ] 查看后端日志：`docker compose logs backend`

3. **WebSocket 失败**
   - [ ] 检查 Nginx 配置
   - [ ] 重启容器：`docker compose restart`
   - [ ] 查看浏览器控制台

4. **性能问题**
   - [ ] 查看资源使用：`docker stats`
   - [ ] 查看系统负载：`htop`
   - [ ] 考虑升级配置

详细解决方案参见：**[故障排查手册](TROUBLESHOOTING.md)**

---

## 📝 部署信息记录

### 服务器信息
- 服务商：`__________________`
- IP 地址：`__________________`
- 区域：`__________________`
- 配置：`__________________`
- 购买日期：`__________________`

### 域名信息（如有）
- 域名：`__________________`
- 注册商：`__________________`
- 到期日期：`__________________`

### 部署信息
- 部署日期：`__________________`
- Docker 版本：`__________________`
- 项目版本：`__________________`

### API 信息
- DeepSeek：✅ 已配置
- Qwen：✅ 已配置
- Doubao：✅ 已配置

---

## ✅ 最终确认

完成以下所有项，即表示部署成功：

- [ ] ✅ 云服务器正常运行
- [ ] ✅ Docker 容器全部 Up 状态
- [ ] ✅ 网站可以访问（电脑 + 手机）
- [ ] ✅ AI 辩论功能正常
- [ ] ✅ 无控制台错误
- [ ] ✅ 已添加到 iPhone 主屏幕

---

## 🎉 恭喜！

您已成功部署 AI 辩论平台！

### 下一步建议：
1. **分享给朋友**：让更多人体验 AI 辩论
2. **添加主屏幕**：在 iPhone 上像 App 一样使用
3. **配置域名**：获得专业的访问地址
4. **启用 HTTPS**：提升安全性
5. **定期维护**：保持系统更新

### 需要帮助？
- 📖 查看文档：`CLOUD_DEPLOYMENT.md`
- 🔧 故障排查：`TROUBLESHOOTING.md`
- 💬 提交问题：GitHub Issues

---

**祝您使用愉快！🎊**
