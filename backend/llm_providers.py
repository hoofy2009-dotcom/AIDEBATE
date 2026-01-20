import os
from abc import ABC, abstractmethod
from typing import List, AsyncGenerator
import openai
import anthropic
from dotenv import load_dotenv
import google.generativeai as genai
import dashscope
# from volcengine.ark import Ark

# Suppress logging warnings for clean output
import logging
logging.getLogger("absl").setLevel(logging.ERROR)

load_dotenv()

class LLMProvider(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[dict]) -> str:
        """根据历史消息生成回复"""
        pass
    
    @abstractmethod
    async def stream_response(self, messages: List[dict]) -> AsyncGenerator[str, None]:
        """根据历史消息流式生成回复"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, model_name: str = "gpt-4o", api_key: str = None):
        self.model_name = model_name
        self.client = openai.AsyncOpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    @property
    def name(self) -> str:
        return "ChatGPT"

    async def generate_response(self, messages: List[dict]) -> str:
        # ...existing code...
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_msgs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error from OpenAI: {str(e)}"

    async def stream_response(self, messages: List[dict]) -> AsyncGenerator[str, None]:
        formatted_msgs = [{"role": "system", "content": "You are a participant in a group debate. Express your opinion clearly, critique others constructively, and try to reach a conclusion."}]
        for m in messages:
            role = "user" if m['role'] == "user" else "assistant"
            content = f"[{m['name']}]: {m['content']}" if m.get('name') else m['content']
            formatted_msgs.append({"role": role, "content": content})

        try:
            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_msgs,
                stream=True
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"Error from OpenAI: {str(e)}"

class DeepSeekProvider(LLMProvider):
    def __init__(self, model_name: str = "deepseek-chat", api_key: str = None):
        self.model_name = model_name
        # DeepSeek 通常兼容 OpenAI SDK
        self.client = openai.AsyncOpenAI(
            api_key=api_key or os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    @property
    def name(self) -> str:
        return "DeepSeek"

    async def generate_response(self, messages: List[dict]) -> str:
        # ...existing code...
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_msgs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error from DeepSeek: {str(e)}"

    async def stream_response(self, messages: List[dict]) -> AsyncGenerator[str, None]:
        formatted_msgs = [{"role": "system", "content": "You are a helpful and sharp AI assistant participating in a debate."}]
        for m in messages:
            role = "user" if m['role'] == "user" else "assistant"
            content = f"[{m['name']}]: {m['content']}" if m.get('name') else m['content']
            formatted_msgs.append({"role": role, "content": content})

        try:
            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_msgs,
                stream=True
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"Error from DeepSeek: {str(e)}"

class ClaudeProvider(LLMProvider):
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620", api_key: str = None):
        self.model_name = model_name
        self.client = anthropic.AsyncAnthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    @property
    def name(self) -> str:
        return "Claude"

    async def generate_response(self, messages: List[dict]) -> str:
        # ...existing code...
        try:
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                system=system_prompt,
                messages=anthropic_msgs
            )
            return response.content[0].text
        except Exception as e:
            return f"Error from Claude: {str(e)}"

    async def stream_response(self, messages: List[dict]) -> AsyncGenerator[str, None]:
        system_prompt = "You are Claude, participating in a group chat debate. Engage with other participants."
        anthropic_msgs = []
        for m in messages:
            role = "user" if m['role'] == "user" else "assistant"
            content = f"[{m['name']}]: {m['content']}" if m.get('name') else m['content']
            anthropic_msgs.append({"role": role, "content": content})

        try:
            async with self.client.messages.stream(
                max_tokens=1024,
                system=system_prompt,
                messages=anthropic_msgs,
                model=self.model_name,
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            yield f"Error from Claude: {str(e)}"

class GrokProvider(LLMProvider):
    def __init__(self, model_name: str = "grok-beta", api_key: str = None):
        self.model_name = model_name
        # Assuming Grok uses OpenAI compatible API endpoint
        self.client = openai.AsyncOpenAI(
            api_key=api_key or os.environ.get("XAI_API_KEY"),
            base_url="https://api.x.ai/v1" 
        )

    @property
    def name(self) -> str:
        return "Grok"

    async def generate_response(self, messages: List[dict]) -> str:
        # ...existing code...
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_msgs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error from Grok: {str(e)}"

    async def stream_response(self, messages: List[dict]) -> AsyncGenerator[str, None]:
        formatted_msgs = [{"role": "system", "content": "You are Grok, a witty AI. Join the debate."}]
        for m in messages:
            role = "user" if m['role'] == "user" else "assistant"
            content = f"[{m['name']}]: {m['content']}" if m.get('name') else m['content']
            formatted_msgs.append({"role": role, "content": content})

        try:
            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_msgs,
                stream=True
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"Error from Grok: {str(e)}"

class GeminiProvider(LLMProvider):
    def __init__(self, model_name: str = "gemini-2.0-flash", api_key: str = None):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    @property
    def name(self) -> str:
        return "Gemini"

    async def generate_response(self, messages: List[dict]) -> str:
        # ...existing code...
        try:
            # We use generate_content for simplicity instead of chat session for stateless request
            response = await self.model.generate_content_async(full_last_prompt)
            return response.text
        except Exception as e:
            return f"Error from Gemini: {str(e)}"

    async def stream_response(self, messages: List[dict]) -> AsyncGenerator[str, None]:
        if not self.model:
            yield "Error: GOOGLE_API_KEY not configured."
            return

        history = []
        for m in messages[:-1]:
            role = "user" if m['role'] == "user" else "model"
            content = f"[{m['name']}]: {m['content']}" if m.get('name') else m['content']
            history.append({"role": role, "parts": [content]})
            
        last_msg = messages[-1]
        last_content = f"[{last_msg['name']}]: {last_msg['content']}" if last_msg.get('name') else last_msg['content']
        system_instruction = "System: You are Gemini, participating in a group debate. Be concise and sharp."
        full_last_prompt = f"{system_instruction}\n\nContext so far:\n{history}\n\nLatest message:\n{last_content}"

        try:
            response = await self.model.generate_content_async(full_last_prompt, stream=True)
            async for chunk in response:
                yield chunk.text
        except Exception as e:
            yield f"Error from Gemini: {str(e)}"

class QwenProvider(LLMProvider):
    def __init__(self, model_name: str = "qwen-turbo", api_key: str = None):
        self.model_name = model_name
        # dashscope.api_key needs to be set globally or passed in call
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
        dashscope.api_key = self.api_key

    @property
    def name(self) -> str:
        return "Qwen"

    async def generate_response(self, messages: List[dict]) -> str:
        # ...existing code...
        try:
            # Using sync call in async wrapper roughly, but dashscope has async call? 
            # For simplicity using standard call. Blocking in async loop is not ideal but works for low traffic.
            response = dashscope.Generation.call(
                model=self.model_name,
                messages=ds_msgs,
                result_format='message',  # set the result to be "message" format.
            )
            if response.status_code == 200:
                return response.output.choices[0].message.content
            else:
                return f"Error from Qwen: {response.code} - {response.message}"
        except Exception as e:
            return f"Error from Qwen: {str(e)}"

    async def stream_response(self, messages: List[dict]) -> AsyncGenerator[str, None]:
        ds_msgs = []
        for m in messages:
            role = "user" if m['role'] == "user" else "assistant"
            content = f"[{m['name']}]: {m['content']}" if m.get('name') else m['content']
            ds_msgs.append({'role': role, 'content': content})
        ds_msgs.insert(0, {'role': 'system', 'content': 'You are Qwen, a helpful assistant in a group debate.'})

        try:
            responses = dashscope.Generation.call(
                model=self.model_name,
                messages=ds_msgs,
                result_format='message',
                stream=True,
                incremental_output=True # Important for getting deltas
            )
            for response in responses:
                if response.status_code == 200:
                    yield response.output.choices[0].message.content
                else:
                    yield f"Error: {response.code} - {response.message}"
        except Exception as e:
            yield f"Error from Qwen: {str(e)}"

class DoubaoProvider(LLMProvider):
    def __init__(self, model_name: str = None, api_key: str = None):
        # For Doubao, model_name should really be the Endpoint ID
        self.api_key = api_key or os.environ.get("VOLCENGINE_API_KEY")
        self.endpoint_id = os.environ.get("DOUBAO_ENDPOINT_ID")
        # Use OpenAI client for Doubao (Compatible mode)
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )

    @property
    def name(self) -> str:
        return "Doubao"

    async def generate_response(self, messages: List[dict]) -> str:
        # ...existing code...
        try:
            if not self.endpoint_id:
                return "Error: DOUBAO_ENDPOINT_ID not configured."

            # Doubao requires the 'model' parameter to be the Endpoint ID
            completion = await self.client.chat.completions.create(
                model=self.endpoint_id,
                messages=formatted_msgs,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error from Doubao: {str(e)}"

    async def stream_response(self, messages: List[dict]) -> AsyncGenerator[str, None]:
        formatted_msgs = [{"role": "system", "content": "You are Doubao, a helpful assistant in a group debate."}]
        for m in messages:
            role = "user" if m['role'] == "user" else "assistant"
            content = f"[{m['name']}]: {m['content']}" if m.get('name') else m['content']
            formatted_msgs.append({"role": role, "content": content})

        try:
            if not self.endpoint_id:
                yield "Error: DOUBAO_ENDPOINT_ID not configured."
                return

            stream = await self.client.chat.completions.create(
                model=self.endpoint_id,
                messages=formatted_msgs,
                stream=True
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"Error from Doubao: {str(e)}"

def get_provider(name: str) -> LLMProvider:
    if "gpt" in name.lower():
        return OpenAIProvider(model_name=name)
    elif "claude" in name.lower():
        return ClaudeProvider(model_name=name)
    elif "deepseek" in name.lower():
        return DeepSeekProvider(model_name=name)
    elif "grok" in name.lower():
        return GrokProvider(model_name=name)
    elif "gemini" in name.lower():
        return GeminiProvider(model_name=name)
    elif "qwen" in name.lower():
        return QwenProvider(model_name=name)
    elif "doubao" in name.lower():
        return DoubaoProvider(model_name=name)
    else:
        # Default fallback
        return OpenAIProvider(model_name="gpt-3.5-turbo")
