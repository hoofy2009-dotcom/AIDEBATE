# 🎭 AI 辩论平台

> 让多个顶尖 AI 同台辩论，碰撞思想火花！

一个支持多 AI 实时辩论的现代化平台，集成 DeepSeek、Qwen（通义千问）、Doubao（豆包）等国产顶尖 AI，支持移动端访问和云端部署。

## ✨ 功能特性

- 🤖 **多 AI 支持**：DeepSeek、Qwen（通义千问）、Doubao（豆包）三大国产 AI
- 🔄 **多轮辩论**：支持 1-5 轮可配置辩论，实时显示当前轮次
- 📝 **智能总结**：辩论结束后可选择任一 AI 生成结论总结
- 🌐 **联网搜索**：集成 DuckDuckGo 实时搜索最新信息
- 💬 **流式响应**：实时打字机效果，体验流畅自然
- 📱 **移动友好**：完美支持 iPhone、iPad 等移动设备
- ☁️ **云端部署**：一键部署到云服务器，24/7 在线访问
- 🎨 **精美 UI**：现代化设计，深色模式，视觉效果出色

## 🚀 快速开始

### 方案 1：本地开发（5分钟）

```bash
# 1. 克隆项目
cd e:\项目\ai-debate

# 2. 配置 API Keys
cd backend
# 编辑 .env 填入你的 API Keys

# 3. 安装后端依赖
pip install -r requirements.txt

# 4. 安装前端依赖
cd ../frontend
npm install

# 5. 启动服务
# 终端 1 - 启动后端
cd backend
python main.py

# 终端 2 - 启动前端
cd frontend
npm run dev
```

访问：http://localhost:5173

### 方案 2：云端部署（推荐 ⭐）

**只需 5 分钟，让你的 AI 辩论平台在云端 24/7 运行！**

📖 查看详细教程：**[⚡ 5分钟快速部署指南](QUICK_START.md)**

```bash
# 1. 连接到云服务器
ssh root@你的服务器IP

# 2. 安装 Docker
curl -fsSL https://get.docker.com | sh

# 3. 上传项目并配置 API Keys
# (参见 QUICK_START.md 详细步骤)

# 4. 一键部署
chmod +x deploy.sh && ./deploy.sh
```

## 📚 完整文档

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [⚡ 快速开始](QUICK_START.md) | 5分钟快速部署指南 | ⭐ 所有用户必读 |
| [☁️ 云端部署](CLOUD_DEPLOYMENT.md) | 详细的云部署教程 | 需要云端部署的用户 |
| [🌐 服务器推荐](SERVER_RECOMMENDATION.md) | 云服务器选择指南 | 首次购买云服务器的用户 |
| [🔧 故障排查](TROUBLESHOOTING.md) | 常见问题解决方案 | 遇到问题时查阅 |

## 🛠️ 技术栈

### 后端
- **FastAPI** 0.115.6 - 现代高性能 Web 框架
- **Uvicorn** 0.34.0 - ASGI 服务器
- **WebSocket** - 实时双向通信
- **ddgs** 9.10.0 - DuckDuckGo 搜索集成

### 前端
- **React** 18 - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 快速构建工具
- **Tailwind CSS** - 实用优先的 CSS 框架

### AI 提供商
- **DeepSeek** - 高性能对话模型
- **Qwen (通义千问)** - 阿里云百炼
- **Doubao (豆包)** - 火山引擎

### 部署
- **Docker** - 容器化
- **Docker Compose** - 多容器编排
- **Nginx** - 反向代理和静态文件服务

## 🎯 使用场景

- 📖 **学习研究**：探索不同 AI 的思维方式和观点差异
- 💡 **决策辅助**：让多个 AI 从不同角度分析问题
- 🎓 **教育培训**：展示 AI 辩论能力，训练批判性思维
- 🎪 **娱乐互动**：观看 AI 之间的精彩辩论
- 🔬 **AI 比较**：对比不同 AI 模型的表现和特点

## 📱 移动端访问

### 本地网络访问

```bash
# 运行脚本获取移动访问地址
cd backend
python get_mobile_url.py
```

会显示二维码，用 iPhone 扫码即可访问！

### 云端访问

部署到云服务器后，直接在 iPhone Safari 打开：
```
http://你的服务器IP
或
https://yourdomain.com
```

**添加到主屏幕**：点击分享 → "添加到主屏幕"，像原生 App 一样使用！

## 🔑 API Keys 获取

### DeepSeek
1. 访问：https://platform.deepseek.com/
2. 注册并登录
3. API Keys → 创建新密钥
4. 复制密钥（格式：`sk-...`）

### Qwen（通义千问）
1. 访问：https://bailian.console.aliyun.com/
2. 开通百炼服务
3. API Key 管理 → 创建密钥
4. 复制密钥（格式：`sk-...`）

### Doubao（豆包）
1. 访问：https://console.volcengine.com/ark
2. 开通火山方舟服务
3. 创建推理接入点
4. 复制 API Key 和 Endpoint ID

## 📂 项目结构

```
ai-debate/
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI 主程序
│   ├── llm_providers.py    # AI 提供商接口
│   ├── web_search.py       # 网络搜索功能
│   ├── requirements.txt    # Python 依赖
│   └── .env                # 环境变量（需创建）
│
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── App.tsx        # 主组件
│   │   └── config.ts      # 配置文件
│   ├── package.json       # Node 依赖
│   └── vite.config.js     # Vite 配置
│
├── docker/                # Docker 配置
│   └── nginx.conf         # Nginx 配置
│
├── Dockerfile.backend     # 后端 Dockerfile
├── Dockerfile.frontend    # 前端 Dockerfile
├── docker-compose.yml     # Docker Compose 配置
├── deploy.sh              # 自动化部署脚本
│
├── .env.production        # 生产环境配置（需创建）
│
└── 文档/
    ├── README.md          # 本文件
    ├── QUICK_START.md     # 快速开始
    ├── CLOUD_DEPLOYMENT.md # 云端部署
    ├── SERVER_RECOMMENDATION.md # 服务器推荐
    └── TROUBLESHOOTING.md  # 故障排查
```

## 🎮 使用示例

1. **开始辩论**
   - 输入辩论主题，如："人工智能是否会取代人类工作？"
   - 选择辩论轮数（1-5轮）
   - 选择总结 AI
   - 可选：启用联网搜索
   - 点击"开始辩论"

2. **观看辩论**
   - 实时查看三个 AI 的观点
   - 查看当前辩论轮次
   - 流式显示，体验流畅

3. **查看总结**
   - 辩论结束后自动生成总结
   - 金色渐变高亮显示
   - 综合各方观点

## 🔧 高级配置

### 修改 AI 模型

编辑 `backend/llm_providers.py`：
```python
# 修改 DeepSeek 模型
DEEPSEEK_MODEL = "deepseek-chat"  # 或其他模型

# 修改 Qwen 模型
QWEN_MODEL = "qwen-turbo"  # 或 qwen-plus, qwen-max
```

### 调整超时时间

编辑 `docker/nginx.conf`：
```nginx
proxy_read_timeout 3600s;  # 增加到 1 小时
```

### 启用 HTTPS

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d yourdomain.com
```

## 📞 技术支持

如遇问题，请查看：
1. **[故障排查手册](TROUBLESHOOTING.md)** - 常见问题解决方案
2. **Docker 日志**：`docker compose logs`
3. **GitHub Issues**：提交问题报告

## 🗺️ 路线图

- [ ] 支持更多 AI 模型（Claude、ChatGPT、Gemini）
- [ ] 用户系统和历史记录
- [ ] 数据持久化（数据库）
- [ ] 辩论录制和回放
- [ ] 多语言支持
- [ ] 实时协作（多用户观看）
- [ ] AI 评分系统
- [ ] 自定义 AI 角色和性格

## 📄 开源协议

本项目采用 MIT 协议开源

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) - 提供高性能 AI 模型
- [阿里云百炼](https://bailian.console.aliyun.com/) - 通义千问 API
- [火山引擎](https://www.volcengine.com/) - 豆包 AI 服务
- [DuckDuckGo](https://duckduckgo.com/) - 隐私友好的搜索引擎

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star！**

Made with ❤️

</div>
