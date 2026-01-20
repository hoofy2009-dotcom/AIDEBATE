import os
import asyncio
from dotenv import load_dotenv
import openai

load_dotenv()

async def test_doubao():
    api_key = os.environ.get("VOLCENGINE_API_KEY")
    endpoint_id = os.environ.get("DOUBAO_ENDPOINT_ID")
    
    print(f"Testing Doubao with API Key: {api_key[:6]}... Endpoint: {endpoint_id}")
    
    client = openai.AsyncOpenAI(
        api_key=api_key,
        base_url="https://ark.cn-beijing.volces.com/api/v3"
    )
    
    try:
        print("Sending request to Doubao...")
        completion = await client.chat.completions.create(
            model=endpoint_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, who are you?"}
            ],
            timeout=30.0 # Add a timeout to see if it hangs
        )
        print("Response received:")
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_doubao())
