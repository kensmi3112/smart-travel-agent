import os
from openai import OpenAI
from core.config import Config

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

def web_search(query: str) -> str:
    """Perform real-time web search"""
    print(f"🔍 Searching the web: {query}")
    
    try:
        response = client.chat.completions.create(
            model=Config.MODEL,
            messages=[
                {"role": "system", "content": "You are a precise research assistant. Summarize the most relevant and current information clearly."},
                {"role": "user", "content": query}
            ],
            max_tokens=700
        )
        result = response.choices[0].message.content.strip()
        return result if result else "No relevant information found."
    except Exception as e:
        return f"Search error: {str(e)}"