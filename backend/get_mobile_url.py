import socket
import qrcode
from io import BytesIO

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        # 创建一个UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到外部地址（不会真正发送数据）
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def generate_qr_code(url):
    """生成二维码（ASCII版本）"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # 打印ASCII二维码
        qr.print_ascii(invert=True)
    except Exception as e:
        print(f"二维码生成失败: {e}")

def main():
    ip = get_local_ip()
    frontend_port = 5173
    backend_port = 8000
    
    frontend_url = f"http://{ip}:{frontend_port}"
    
    print("=" * 60)
    print("📱 移动设备访问指南")
    print("=" * 60)
    print()
    print(f"✅ 您的电脑 IP 地址: {ip}")
    print()
    print("📍 访问地址:")
    print(f"   前端: {frontend_url}")
    print(f"   后端: http://{ip}:{backend_port}")
    print()
    print("🔧 在 iPhone 上访问:")
    print(f"   1. 确保 iPhone 和电脑在同一 Wi-Fi 网络")
    print(f"   2. 在 iPhone Safari 浏览器中打开:")
    print(f"      {frontend_url}")
    print()
    print("📱 扫描下方二维码快速访问:")
    print()
    
    # 生成二维码
    generate_qr_code(frontend_url)
    
    print()
    print("=" * 60)
    print("⚠️  注意事项:")
    print("   • 确保 Windows 防火墙允许 5173 和 8000 端口")
    print("   • 如果无法访问，请关闭防火墙或添加规则")
    print("   • 使用 Safari 浏览器效果最佳")
    print("=" * 60)
    print()
    print("🔥 防火墙配置命令（管理员身份运行）:")
    print(f"   netsh advfirewall firewall add rule name=\"AI Debate Frontend\" dir=in action=allow protocol=TCP localport={frontend_port}")
    print(f"   netsh advfirewall firewall add rule name=\"AI Debate Backend\" dir=in action=allow protocol=TCP localport={backend_port}")
    print()

if __name__ == "__main__":
    main()
