import anthropic
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = anthropic.Anthropic()

async def summarize_text(text: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text in 2-3 sentences:\n\n{text}"
            }
        ]
    )
    return message.content[0].text.strip()




