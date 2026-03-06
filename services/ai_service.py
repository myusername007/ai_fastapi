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
                "content": f"Summarize the following text in 2-3 sentences, do not write summarize:... etc, just text:\n\n{text}"
            }
        ]
    )
    return message.content[0].text.strip()


async def analyze_sentiment(text: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=10,
        messages=[
            {
                "role": "user",
                "content": f"Analyze the sentiment of this text. Reply with only one word: positive, negative, or neutral.\n\n{text}"
            }
        ]
    )
    return message.content[0].text.strip().lower()


async def ask_question(text: str, question: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system="You are a helpful assistant. Answer questions based only on the provided text. If the answer is not in the text, say so.",
        messages=[
            {
                "role": "user",
                "content": f"Text:\n{text}\n\nQuestion: {question}"
            }
        ]
    )
    return message.content[0].text

async def chat(text: str, messages: list) -> str:
    messages_with_context = messages.copy()
    messages_with_context[0]["content"] = (
        f"Document:\n{text}\n\n{messages_with_context[0]['content']}"
    )
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system="Answer questions based only on the provided document.",
        messages=messages_with_context
    )
    return message.content[0].text