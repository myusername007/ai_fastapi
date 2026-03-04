from fastapi import FastAPI, HTTPException
from services.ai_service import summarize_text, analyze_sentiment
from schemas import SummarizeRequest, SummarizeResponse, SentimentRequest, SentimentResponse

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