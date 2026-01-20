import asyncio
import os
from dotenv import load_dotenv
from llm_providers import DoubaoProvider, DeepSeekProvider, QwenProvider

load_dotenv()

async def test_debate_scenario():
    print("=" * 60)
    print("测试豆包在多轮辩论场景中的表现")
    print("=" * 60)
    
    # 模拟辩论历史
    chat_history = [
        {"role": "user", "name": "User", "content": "人工智能是否会取代人类工作？"},
        {"role": "assistant", "name": "DeepSeek", "content": "我认为AI会取代部分重复性工作，但创造性工作难以替代。"},
        {"role": "assistant", "name": "Qwen", "content": "不完全同意。AI可能会改变工作形式，但会创造新岗位。"},
    ]
    
    provider = DoubaoProvider()
    
    print(f"\n🤖 测试 {provider.name}")
    print(f"📝 当前对话历史: {len(chat_history)} 条消息")
    print("\n" + "=" * 60)
    print("豆包的回复:")
    print("=" * 60)
    
    try:
        full_response = ""
        chunk_count = 0
        
        async for chunk in provider.stream_response(chat_history):
            full_response += chunk
            chunk_count += 1
            print(chunk, end="", flush=True)
        
        print("\n" + "=" * 60)
        print(f"\n📊 统计:")
        print(f"   - 收到块数: {chunk_count}")
        print(f"   - 总字符数: {len(full_response)}")
        print(f"   - 是否只有表情: {'❌ 是' if len(full_response) < 10 else '✅ 否'}")
        
        if chunk_count < 5:
            print(f"\n⚠️  警告: 块数太少 ({chunk_count})，可能出现问题!")
            
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_debate_scenario())
