from fastapi import FastAPI, HTTPException
from services.ai_service import summarize_text
from schemas import SummarizeRequest, SummarizeResponse

app = FastAPI()

@app.post("/summarize", response_model=SummarizeResponse)
async def sum_response(text: str):
    response = await summarize_text(text=text)
    if not response:
        raise HTTPException(
            status_code=404,
            detail="Response not found"
        )
    return SummarizeResponse(summary=response)
