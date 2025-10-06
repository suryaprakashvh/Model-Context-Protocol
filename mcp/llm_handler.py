from groq import Groq
from mcp.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(query: str) -> str:
    """
    Calls Groq API to answer general questions.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content
