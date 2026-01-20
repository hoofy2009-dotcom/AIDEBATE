# AI 辩论平台 - 远程部署脚本
# 使用方法: .\deploy-remote.ps1

$SERVER_IP = "8.222.242.128"
$SERVER_USER = "root"
$PROJECT_PATH = "e:\项目\ai-debate"

Write-Host "🚀 AI 辩论平台 - 远程部署脚本" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 SSH 连接
Write-Host "📡 测试服务器连接..." -ForegroundColor Yellow
$pingResult = Test-Connection -ComputerName $SERVER_IP -Count 2 -Quiet
if (-not $pingResult) {
    Write-Host "❌ 无法连接到服务器 $SERVER_IP" -ForegroundColor Red
    Write-Host "请检查:" -ForegroundColor Yellow
    Write-Host "  1. 服务器IP是否正确" -ForegroundColor Yellow
    Write-Host "  2. 服务器是否运行" -ForegroundColor Yellow
    Write-Host "  3. 防火墙是否开放" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ 服务器可达" -ForegroundColor Green
Write-Host ""

# 上传项目文件
Write-Host "📤 上传项目文件到服务器..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟，请耐心等待..." -ForegroundColor Yellow
Write-Host ""

scp -r "$PROJECT_PATH" "${SERVER_USER}@${SERVER_IP}:/root/"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 文件上传失败" -ForegroundColor Red
    Write-Host "请确保:" -ForegroundColor Yellow
    Write-Host "  1. SSH密码正确" -ForegroundColor Yellow
    Write-Host "  2. 有足够的磁盘空间" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ 文件上传成功" -ForegroundColor Green
Write-Host ""

# 项目已上传，接下来需要手动配置

Write-Host "📋 接下来需要您手动完成以下步骤:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣ 连接到服务器:" -ForegroundColor Yellow
Write-Host "   ssh root@$SERVER_IP" -ForegroundColor White
Write-Host ""
Write-Host "2️⃣ 配置 API Keys:" -ForegroundColor Yellow
Write-Host "   cd /root/ai-debate" -ForegroundColor White
Write-Host "   nano .env.production" -ForegroundColor White
Write-Host ""
Write-Host "   填入以下内容:" -ForegroundColor Yellow
Write-Host "   DEEPSEEK_API_KEY=sk-your-key-here" -ForegroundColor White
Write-Host "   DASHSCOPE_API_KEY=sk-your-key-here" -ForegroundColor White
Write-Host "   VOLCENGINE_API_KEY=your-key-here" -ForegroundColor White
Write-Host "   DOUBAO_ENDPOINT_ID=ep-m-20260119234219-sqd59" -ForegroundColor White
Write-Host ""
Write-Host "   保存: Ctrl+O, Enter, Ctrl+X" -ForegroundColor Yellow
Write-Host ""
Write-Host "3️⃣ 运行部署:" -ForegroundColor Yellow
Write-Host "   chmod +x deploy.sh" -ForegroundColor White
Write-Host "   ./deploy.sh" -ForegroundColor White
Write-Host ""
Write-Host "完成后访问: http://$SERVER_IP" -ForegroundColor Green
Write-Host ""

# 询问是否立即连接
$response = Read-Host "是否现在连接到服务器? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "正在连接到服务器..." -ForegroundColor Green
    $sshCommand = "$SERVER_USER@$SERVER_IP"
    ssh $sshCommand
}
