from typing import List, Optional, Literal
from pydantic import BaseModel
import time

class Message(BaseModel):
    role: str  # "user", "assistant" (for generic AI), or specific agent names like "Claude", "ChatGPT", "DeepSeek"
    name: Optional[str] = None # 具体显示的名称，例如 "DeepSeek V3"
    content: str
    timestamp: float = time.time()

class DebateRequest(BaseModel):
    topic: str
    selected_agents: List[str] # ["gpt-4o", "claude-3-5-sonnet", "deepseek-chat", "grok-beta"]
    rounds: int = 3 # 讨论轮数

class DebateResponse(BaseModel):
    status: str
    message: str
