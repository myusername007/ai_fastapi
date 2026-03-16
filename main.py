from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import anthropic
from services.ai_service import (
    summarize_text, 
    analyze_sentiment, 
    ask_question, chat, 
    session_chat
)
from services.ai_service import client

from schemas import (
    SummarizeRequest, 
    SummarizeResponse, 
    SentimentRequest, 
    SentimentResponse, 
    AskRequest, 
    AskResponse, 
    Message, 
    ChatRequest, 
    ChatResponse,
    SessionChatRequest,
    SessionChatResponse
)
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.post("/summarize", response_model=SummarizeResponse)
async def sum_response(request: SummarizeRequest):
    response = await summarize_text(text=request.text)
    if not response:
        raise HTTPException(
            status_code=404,
            detail="Response not found"
        )
    return SummarizeResponse(summary=response)

@app.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sent(request: SentimentRequest):
    response = await analyze_sentiment(text=request.text)
    if not response:
        raise HTTPException(
            status_code=404,
            detail="Response not found"
        )
    return SentimentResponse(sentiment=response)

@app.post("/ask", response_model=AskResponse)
async def ask_quest(request: AskRequest):
    response = await ask_question(text=request.text, question=request.question)
    if not response:
        raise HTTPException(
            status_code=404,
            detail="Response not found"
        )
    return AskResponse(answer=response)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    response = await chat(text=request.text, messages=request.messages)
    if not response:
         raise HTTPException(
            status_code=404,
            detail="Response not found"
        )
    updated_messages = request.messages + [
        Message(role="assistant", content=response)
    ]
    return ChatResponse(answer=response, messages=updated_messages)

@app.post("/session-chat", response_model=SessionChatResponse)
async def session_chat_end(request: SessionChatRequest):
    session_id, answer = await session_chat(
        session_id=request.session_id,
        text=request.text,
        message=request.message
    )
    if not answer:
        raise HTTPException(
            status_code=404,
            detail="Response not found"
        )
    
    return SessionChatResponse(session_id=session_id, answer=answer)

@app.post("/stream")
async def stream_response(request: SummarizeRequest):
    def generate():
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            messages=[
                {"role": "user", "content": request.text}
            ]
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/plain")


@app.post("/stream-summary")
async def stream_summary_response(request: SummarizeRequest):
    def generate():
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system="You are a helpful assistant. Summarize the provided text concisely.",
            messages=[
                {"role": "user", "content": request.text}
            ]
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/plain")



