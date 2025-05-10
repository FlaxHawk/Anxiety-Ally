from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class JournalEntryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    mood_id: Optional[str] = None

class JournalEntryCreate(JournalEntryBase):
    tags: Optional[List[str]] = []
    image_urls: Optional[List[str]] = []

class JournalEntryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    mood_id: Optional[str] = None
    tags: Optional[List[str]] = None
    image_urls: Optional[List[str]] = None

class JournalEntryInDB(JournalEntryBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    sentiment_score: Optional[float] = None
    tags: List[str] = []
    image_urls: List[str] = []

class JournalEntryResponse(JournalEntryInDB):
    pass

class JournalAnalysis(BaseModel):
    entry_id: str
    sentiment_score: float
    sentiment_label: str
    keywords: List[str]
    suggestions: Optional[List[str]] = None 