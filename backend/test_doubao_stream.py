import asyncio
import os
from dotenv import load_dotenv
from llm_providers import DoubaoProvider

load_dotenv()

async def test_doubao():
    print("=" * 50)
    print("测试豆包流式响应")
    print("=" * 50)
    
    # 检查配置
    api_key = os.environ.get("VOLCENGINE_API_KEY")
    endpoint_id = os.environ.get("DOUBAO_ENDPOINT_ID")
    
    print(f"\n📋 配置检查:")
    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: ❌ 未配置")
    print(f"Endpoint ID: {endpoint_id}")
    
    if not api_key or not endpoint_id:
        print("\n❌ 错误: 请检查 .env 文件中的 VOLCENGINE_API_KEY 和 DOUBAO_ENDPOINT_ID")
        return
    
    # 创建 Provider
    provider = DoubaoProvider()
    print(f"\n🤖 Provider 名称: {provider.name}")
    
    # 测试消息
    test_messages = [
        {"role": "user", "name": "User", "content": "请简单介绍一下你自己，不超过50字。"}
    ]
    
    print("\n📤 发送测试消息...")
    print("=" * 50)
    
    try:
        full_response = ""
        chunk_count = 0
        
        async for chunk in provider.stream_response(test_messages):
            full_response += chunk
            chunk_count += 1
            print(chunk, end="", flush=True)
        
        print("\n" + "=" * 50)
        print(f"\n✅ 测试成功!")
        print(f"📊 统计:")
        print(f"   - 收到块数: {chunk_count}")
        print(f"   - 总字符数: {len(full_response)}")
        print(f"   - 完整回复: {full_response}")
        
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_doubao())
