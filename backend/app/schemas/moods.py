from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MoodBase(BaseModel):
    score: int = Field(..., ge=1, le=10, description="Mood score from 1-10")
    notes: Optional[str] = None

class MoodCreate(MoodBase):
    timestamp: Optional[datetime] = None
    
class MoodUpdate(BaseModel):
    score: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None

class MoodInDB(MoodBase):
    id: str
    user_id: str
    timestamp: datetime
    created_at: datetime

class MoodResponse(MoodInDB):
    pass

class MoodAggregation(BaseModel):
    period: str  # 'day', 'week', 'month'
    data: List[dict]
    average_score: float 