# 快速上传脚本 - 只上传必要文件
$SERVER = "8.222.242.128"

Write-Host "=== 开始上传必要文件到服务器 ===" -ForegroundColor Green

# 创建临时目录
$tempDir = "ai-debate-minimal"
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }
New-Item -ItemType Directory -Path $tempDir | Out-Null

Write-Host "1. 复制必要文件..." -ForegroundColor Yellow

# 复制必要的文件和目录
Copy-Item "docker-compose.yml" $tempDir
Copy-Item "Dockerfile.backend" $tempDir
Copy-Item "Dockerfile.frontend" $tempDir
Copy-Item "deploy.sh" $tempDir
Copy-Item ".dockerignore" $tempDir
Copy-Item ".env.production" $tempDir

# 复制 docker 目录
Copy-Item "docker" $tempDir -Recurse

# 复制 backend（排除 __pycache__）
New-Item -ItemType Directory -Path "$tempDir\backend" | Out-Null
Get-ChildItem "backend" -File | Copy-Item -Destination "$tempDir\backend"

# 复制 frontend（排除 node_modules）
Write-Host "2. 复制前端文件..." -ForegroundColor Yellow
Copy-Item "frontend" $tempDir -Recurse -Exclude "node_modules","dist",".vite"

Write-Host "3. 上传到服务器..." -ForegroundColor Yellow
scp -r $tempDir root@${SERVER}:/root/ai-debate

Write-Host "4. 清理临时文件..." -ForegroundColor Yellow
Remove-Item $tempDir -Recurse -Force

Write-Host "`n=== 上传完成！===" -ForegroundColor Green
Write-Host "现在 SSH 到服务器继续部署：" -ForegroundColor Cyan
Write-Host "ssh root@$SERVER" -ForegroundColor White
