from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print(client)

def generate_response(query, context):
    prompt = f"""
You are an e-commerce support assistant.

Use ONLY the provided context.

Context:
{context}

User Query:
{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text