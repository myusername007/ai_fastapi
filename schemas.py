from pydantic import BaseModel
from typing import List

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str

class AskRequest(BaseModel):
    text: str
    question: str

class AskResponse(BaseModel):
    answer: str

class Message(BaseModel):
    role: str #"user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    text: str 
    messages: List[Message] #history

class ChatResponse(BaseModel):
    answer: str
    messages: List[Message] #updated history