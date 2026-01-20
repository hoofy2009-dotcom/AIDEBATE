# AI 辩论平台 - 远程部署脚本
# 使用方法: .\upload-to-server.ps1

$SERVER_IP = "8.222.242.128"
$SERVER_USER = "root"
$PROJECT_PATH = "e:\项目\ai-debate"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "AI 辩论平台 - 远程部署脚本" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查服务器连接
Write-Host "测试服务器连接..." -ForegroundColor Yellow
$pingResult = Test-Connection -ComputerName $SERVER_IP -Count 2 -Quiet
if (-not $pingResult) {
    Write-Host "无法连接到服务器 $SERVER_IP" -ForegroundColor Red
    exit 1
}
Write-Host "服务器可达" -ForegroundColor Green
Write-Host ""

# 上传项目文件
Write-Host "上传项目文件到服务器..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟，请耐心等待..." -ForegroundColor Yellow
Write-Host ""

scp -r $PROJECT_PATH root@${SERVER_IP}:/root/

if ($LASTEXITCODE -ne 0) {
    Write-Host "文件上传失败" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "文件上传成功" -ForegroundColor Green
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "接下来需要手动完成:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 连接到服务器:" -ForegroundColor Yellow
Write-Host "   ssh root@$SERVER_IP" -ForegroundColor White
Write-Host ""
Write-Host "2. 配置 API Keys:" -ForegroundColor Yellow
Write-Host "   cd /root/ai-debate" -ForegroundColor White
Write-Host "   nano .env.production" -ForegroundColor White
Write-Host ""
Write-Host "   填入内容:" -ForegroundColor Yellow
Write-Host "   DEEPSEEK_API_KEY=sk-your-key" -ForegroundColor White
Write-Host "   DASHSCOPE_API_KEY=sk-your-key" -ForegroundColor White
Write-Host "   VOLCENGINE_API_KEY=your-key" -ForegroundColor White
Write-Host "   DOUBAO_ENDPOINT_ID=ep-m-20260119234219-sqd59" -ForegroundColor White
Write-Host ""
Write-Host "   保存: Ctrl+O, Enter, Ctrl+X" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. 运行部署:" -ForegroundColor Yellow
Write-Host "   chmod +x deploy.sh" -ForegroundColor White
Write-Host "   ./deploy.sh" -ForegroundColor White
Write-Host ""
Write-Host "完成后访问: http://$SERVER_IP" -ForegroundColor Green
Write-Host ""
