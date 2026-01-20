import asyncio
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
from schemas import DebateRequest, Message
from llm_providers import get_provider
from web_search import WebSearcher

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# 模拟存储会话历史
chat_history: List[dict] = []

@app.websocket("/ws/debate")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            
            # 用户发送的消息
            user_msg = Message(
                role="user",
                name="User",
                content=data_json.get("content"),
                timestamp=data_json.get("timestamp")
            )
            chat_history.append(user_msg.dict())
            
            # 广播用户的消息给所有（虽然主要是给自己看回显）
            await manager.broadcast({"type": "message", "data": user_msg.dict()})

            # 触发 AI 讨论逻辑
            # 从请求中读取，或者默认全选
            req_agents = data_json.get("agents", [])
            req_rounds = data_json.get("rounds", 1)  # 获取轮数，默认1轮
            req_summarizer = data_json.get("summarizer", "deepseek-chat")  # 获取总结者
            enable_web_search = data_json.get("enable_web_search", False)  # 是否启用联网搜索
            
            # 如果启用了联网搜索，先搜索相关信息
            search_context = ""
            if enable_web_search:
                try:
                    await manager.broadcast({
                        "type": "message",
                        "data": {
                            "role": "system",
                            "content": "🌐 正在搜索互联网相关信息..."
                        }
                    })
                    
                    searcher = WebSearcher()
                    search_results = searcher.search(user_msg.content, max_results=5)
                    search_context = searcher.format_search_results(search_results)
                    
                    # 将搜索结果添加到历史记录
                    search_msg = Message(
                        role="system",
                        name="WebSearch",
                        content=search_context
                    )
                    chat_history.append(search_msg.dict())
                    
                    await manager.broadcast({
                        "type": "message",
                        "data": {
                            "role": "system",
                            "content": f"✓ 已搜索到 {len(search_results)} 条相关信息，AI 将基于最新互联网资料进行辩论"
                        }
                    })
                    
                except Exception as search_err:
                    print(f"Search error: {search_err}")
                    await manager.broadcast({
                        "type": "message",
                        "data": {
                            "role": "system",
                            "content": f"⚠️ 搜索失败: {str(search_err)}，将基于AI训练数据进行辩论"
                        }
                    })
            
            # 如果前端没传 agents 列表，或者列表为空，我们就在后端动态决定使用哪些
            # 逻辑：检查环境变量，哪个 Key 存在就启用哪个 Agent
            if not req_agents:
                available_agents = []
                # 暂时注释掉无法付费的 AI
                # if os.environ.get("OPENAI_API_KEY") and "your_" not in os.environ.get("OPENAI_API_KEY"):
                #     available_agents.append("gpt-4o")
                # if os.environ.get("ANTHROPIC_API_KEY") and "your_" not in os.environ.get("ANTHROPIC_API_KEY"):
                #     available_agents.append("claude-3-5-sonnet")
                # if os.environ.get("XAI_API_KEY") and "your_" not in os.environ.get("XAI_API_KEY"):
                #     available_agents.append("grok-beta")
                # if os.environ.get("GOOGLE_API_KEY") and "your_" not in os.environ.get("GOOGLE_API_KEY"):
                #     available_agents.append("gemini-2.0-flash")

                if os.environ.get("DEEPSEEK_API_KEY") and "your_" not in os.environ.get("DEEPSEEK_API_KEY"):
                    available_agents.append("deepseek-chat")
                
                if os.environ.get("DASHSCOPE_API_KEY") and "your_" not in os.environ.get("DASHSCOPE_API_KEY"):
                    available_agents.append("qwen-turbo")
                
                if os.environ.get("VOLCENGINE_API_KEY") and "your_" not in os.environ.get("VOLCENGINE_API_KEY"):
                    available_agents.append("doubao-pro-32k")

                # 如果一个 key 都没有，就 fallback 到全选（即使会报错，方便用户知道有哪些）
                if not available_agents:
                    # available_agents = ["deepseek-chat", "qwen-turbo", "doubao-pro-32k"]
                     available_agents = ["deepseek-chat"] # 最低保底
                
                selected_agents = available_agents
            else:
                selected_agents = req_agents

            # 多轮辩论循环
            for round_num in range(1, req_rounds + 1):
                # 广播当前轮数开始
                await manager.broadcast({
                    "type": "round_start",
                    "round": round_num,
                    "total_rounds": req_rounds
                })
                
                # 添加轮次分隔消息
                if round_num > 1:
                    await manager.broadcast({
                        "type": "message",
                        "data": {
                            "role": "system",
                            "content": f"━━━━━━━━━━━━━ 第 {round_num} 轮辩论开始 ━━━━━━━━━━━━━"
                        }
                    })

                # 异步触发每个 Agent 的回复
                # 为了模拟群聊感觉，我们串行让它们发言，并在发言前广播 "正在输入..."
                
                for agent_key in selected_agents:
                    try:
                        provider = get_provider(agent_key)
                        
                        # 广播 typing 状态
                        await manager.broadcast({
                            "type": "typing",
                            "agent": provider.name,
                            "status": True
                        })

                        # 初始化 AI 消息（空内容）让前端准备接收
                        agent_msg_ref = Message(
                            role="assistant",
                            name=provider.name,
                            content=""
                        )
                        await manager.broadcast({"type": "stream_start", "data": agent_msg_ref.dict()})

                        full_response = ""
                        try:
                             # 使用流式调用
                            async for chunk in provider.stream_response(chat_history):
                                if chunk:
                                    full_response += chunk
                                    # 广播增量内容
                                    await manager.broadcast({
                                        "type": "stream_delta", 
                                        "agent": provider.name,
                                        "delta": chunk
                                    })
                        except Exception as stream_err:
                            full_response += f"\n[Error: {stream_err}]"
                            await manager.broadcast({
                                        "type": "stream_delta", 
                                        "agent": provider.name,
                                        "delta": f"\n[Error: {stream_err}]"
                            })

                        # 停止 typing
                        await manager.broadcast({
                            "type": "typing",
                            "agent": provider.name,
                            "status": False
                        })
                        
                        agent_msg_ref.content = full_response
                        # 存入历史
                        chat_history.append(agent_msg_ref.dict())
                        # 结束本次流
                        await manager.broadcast({"type": "stream_end", "agent": provider.name})
                        
                    except Exception as e:
                        # 如果 Provider 初始化本身都失败了
                        print(f"Agent Loop Error: {e}")
                        await manager.broadcast({
                            "type": "typing",
                            "agent": agent_key,
                            "status": False
                        })
                        await manager.broadcast({
                            "type": "message",
                            "data": {
                                "role": "assistant",
                                "name": provider.name,
                                "content": f"[{provider.name} (Simulation)]: I see your point regarding '{user_msg.content}'. However, considering the data... (Error: config API Key to see real response)"
                            }
                        })
                        chat_history.append({
                            "role": "assistant",
                            "name": provider.name,
                            "content": f"[{provider.name} (Simulation)]: I see your point regarding '{user_msg.content}'. However, considering the data... (Error: config API Key to see real response)",
                            "timestamp": data_json.get("timestamp")
                        })
                
                # 广播当前轮次结束
                await manager.broadcast({
                    "type": "round_end",
                    "round": round_num
                })
            
            # 所有轮次完成
            await manager.broadcast({
                "type": "debate_complete",
                "total_rounds": req_rounds
            })
            await manager.broadcast({
                "type": "message",
                "data": {
                    "role": "system",
                    "content": f"✓ 辩论已完成 ({req_rounds} 轮)，正在生成总结..."
                }
            })
            
            # 生成辩论总结
            try:
                summarizer_provider = get_provider(req_summarizer)
                
                # 构建总结提示词
                summary_prompt = {
                    "role": "user",
                    "name": "System",
                    "content": f"请作为辩论总结者，对以上 {req_rounds} 轮关于「{user_msg.content}」的辩论进行全面总结。要求：\n1. 概括各方的核心观点\n2. 分析争议焦点\n3. 给出综合性结论\n4. 字数控制在300-500字"
                }
                chat_history.append(summary_prompt)
                
                # 广播总结开始
                await manager.broadcast({
                    "type": "message",
                    "data": {
                        "role": "system",
                        "content": f"━━━━━━━━━━━━━ 📊 辩论总结 ({summarizer_provider.name}) ━━━━━━━━━━━━━"
                    }
                })
                
                # 流式生成总结
                summary_msg_ref = Message(
                    role="assistant",
                    name=f"{summarizer_provider.name} (总结)",
                    content=""
                )
                await manager.broadcast({"type": "stream_start", "data": summary_msg_ref.dict()})
                
                full_summary = ""
                async for chunk in summarizer_provider.stream_response(chat_history):
                    if chunk:
                        full_summary += chunk
                        await manager.broadcast({
                            "type": "stream_delta",
                            "agent": f"{summarizer_provider.name} (总结)",
                            "delta": chunk
                        })
                
                summary_msg_ref.content = full_summary
                chat_history.append(summary_msg_ref.dict())
                await manager.broadcast({"type": "stream_end", "agent": f"{summarizer_provider.name} (总结)"})
                
                # 最终完成消息
                await manager.broadcast({
                    "type": "message",
                    "data": {
                        "role": "system",
                        "content": "✅ 辩论与总结全部完成！"
                    }
                })
                
            except Exception as summary_err:
                print(f"Summary Error: {summary_err}")
                await manager.broadcast({
                    "type": "message",
                    "data": {
                        "role": "system",
                        "content": f"总结生成失败: {str(summary_err)}"
                    }
                })
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        try:
            await manager.broadcast({"type": "message", "data": {"role": "system", "content": f"Server Error: {str(e)}"}})
        except:
            pass
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    # Use string reference for reload to work
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
