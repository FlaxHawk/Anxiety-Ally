from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any, Optional

from app.routers.auth import get_current_user
from app.services.ai import chat_with_bot, analyze_sentiment
from pydantic import BaseModel, Field

router = APIRouter(prefix="/ai", tags=["ai"])

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    history: Optional[List[ChatMessage]] = Field(None, description="Chat history")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Assistant response")
    suggestions: List[str] = Field(default_factory=list, description="Follow-up suggestions")

class SentimentRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")

class SentimentResponse(BaseModel):
    score: float = Field(..., description="Sentiment score (0 to 1, higher is more positive)")
    label: str = Field(..., description="Sentiment label (POSITIVE or NEGATIVE)")
    keywords: List[str] = Field(default_factory=list, description="Extracted keywords")
    suggestions: Optional[List[str]] = Field(None, description="Suggestions based on sentiment")

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user = Depends(get_current_user)
):
    """
    Chat with the CBT-trained assistant
    """
    # Convert history to the format expected by the AI service
    history = []
    if request.history:
        history = [{"role": msg.role, "content": msg.content} for msg in request.history]
    
    response = await chat_with_bot(request.message, history)
    
    return ChatResponse(
        response=response["response"],
        suggestions=response.get("suggestions", [])
    )

@router.post("/sentiment", response_model=SentimentResponse)
async def analyze_text_sentiment(
    request: SentimentRequest,
    current_user = Depends(get_current_user)
):
    """
    Analyze sentiment of text
    """
    result = await analyze_sentiment(request.text)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sentiment analysis failed"
        )
    
    return SentimentResponse(
        score=result["score"],
        label=result["label"],
        keywords=result["keywords"],
        suggestions=result.get("suggestions")
    )

# Breathing exercise endpoint
class BreathingExercise(BaseModel):
    name: str = Field(..., description="Name of the breathing exercise")
    description: str = Field(..., description="Description of the exercise")
    inhale_duration: int = Field(..., description="Duration of inhale in seconds")
    hold_duration: int = Field(..., description="Duration of hold in seconds", ge=0)
    exhale_duration: int = Field(..., description="Duration of exhale in seconds")
    cycles: int = Field(..., description="Recommended number of cycles", ge=1)

@router.get("/breathing-exercises", response_model=List[BreathingExercise])
async def get_breathing_exercises():
    """
    Get a list of guided breathing exercises
    """
    # These could be stored in a database, but for simplicity they're hardcoded here
    breathing_exercises = [
        {
            "name": "4-7-8 Breathing",
            "description": "The 4-7-8 technique forces your mind and body to focus on regulating your breath, rather than replaying your worries. Close your eyes and inhale through your nose for 4 seconds, hold your breath for 7 seconds, then exhale slowly through your mouth for 8 seconds.",
            "inhale_duration": 4,
            "hold_duration": 7,
            "exhale_duration": 8,
            "cycles": 4
        },
        {
            "name": "Box Breathing",
            "description": "Box breathing is a technique used to calm yourself down with a simple 4 second rotation of breathing in, holding your breath, breathing out, holding your breath, and repeating.",
            "inhale_duration": 4,
            "hold_duration": 4,
            "exhale_duration": 4,
            "cycles": 5
        },
        {
            "name": "Deep Breathing",
            "description": "Deep breathing is a simple yet powerful relaxation technique. It's easy to learn, can be practiced almost anywhere, and provides a quick way to reduce stress levels.",
            "inhale_duration": 5,
            "hold_duration": 0,
            "exhale_duration": 5,
            "cycles": 10
        }
    ]
    
    return breathing_exercises

@router.post("/chat")
def chat():
    return {"msg": "Chatbot endpoint"}

@router.post("/sentiment")
def sentiment():
    return {"msg": "Sentiment analysis endpoint"} 