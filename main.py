from fastapi import FastAPI, HTTPException
from services.ai_service import summarize_text, analyze_sentiment, ask_question, chat
from schemas import SummarizeRequest, SummarizeResponse, SentimentRequest, SentimentResponse, AskRequest, AskResponse, Message, ChatRequest, ChatResponse

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

