import anthropic
import os
from dotenv import load_dotenv
import re
import uuid
from redis_client import redis_client
import json

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
    messages_with_context = [
        {"role": m.role, "content": m.content} for m in messages
    ]
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

async def session_chat(session_id: str, text: str, message: str ) -> tuple[str, str]:
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Дістаємо історію з Redis (рядок) і конвертуємо в список
    history_raw = await redis_client.get(f"chat:{session_id}")
    history = json.loads(history_raw) if history_raw else []

    # Додаємо нове повідомлення юзера
    history.append({"role": "user", "content": message})

    # Викликаємо Claude з повною історією
    # Перше повідомлення має містити текст документу
    messages_with_context = history.copy()
    messages_with_context[0]["content"] = f"Document:\n{text}\n\n{messages_with_context[0]['content']}"

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system="Answer questions based only on the provided document.",
        messages=messages_with_context
    )
    
    answer = response.content[0].text

    history.append({"role": "assistant", "content": answer})
    await redis_client.set(f"chat:{session_id}", json.dumps(history), ex=3600)

    return session_id, answer


async def analyze_text(text: str) -> dict:
    extract_tool = {
    "name": "extract_info",
    "description": "Extract structured information from text",
    "input_schema": {
        "type": "object",
        "properties": {
            "sentiment": {
                "type": "string",
                "enum": ["positive", "negative", "neutral"]
            },
            "summary": {"type": "string"},
            "key_topics": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["sentiment", "summary", "key_topics"]
    }
    }

    response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=512,
    tools=[extract_tool],
    tool_choice={"type": "tool", "name": "extract_info"},  # примусово викликати цей tool
    messages=[{"role": "user", "content": text}]
    )

    # Результат завжди tool_use блок
    tool_use = next(b for b in response.content if b.type == "tool_use")
    result = tool_use.input  # це вже dict з валідним JSON
    return result