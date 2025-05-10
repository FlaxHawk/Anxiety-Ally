from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

from app.schemas.journals import (
    JournalEntryCreate, 
    JournalEntryUpdate, 
    JournalEntryResponse, 
    JournalAnalysis
)
from app.routers.auth import get_current_user
from app.services.supabase import get_supabase_client
from app.services.ai import analyze_sentiment

router = APIRouter(prefix="/journals", tags=["journals"])

@router.post("/", response_model=JournalEntryResponse)
async def create_journal_entry(
    entry: JournalEntryCreate, 
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    new_entry = {
        "title": entry.title,
        "content": entry.content,
        "mood_id": entry.mood_id,
        "user_id": current_user["id"],
        "created_at": datetime.utcnow().isoformat(),
        "tags": entry.tags,
        "image_urls": entry.image_urls
    }
    
    response = supabase.table('journal_entries').insert(new_entry).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create journal entry"
        )
    
    created_entry = response.data[0]
    
    # Queue sentiment analysis as a background task
    # In a production environment, you'd use a message queue like Celery
    # For simplicity, we're doing it synchronously here
    try:
        sentiment_data = await analyze_sentiment(created_entry["content"])
        if sentiment_data:
            supabase.table('journal_entries').update({
                "sentiment_score": sentiment_data["score"]
            }).eq('id', created_entry["id"]).execute()
            created_entry["sentiment_score"] = sentiment_data["score"]
    except Exception:
        # Continue even if sentiment analysis fails
        pass
    
    return created_entry

@router.get("/", response_model=List[JournalEntryResponse])
async def get_journal_entries(
    current_user = Depends(get_current_user),
    skip: int = 0,
    limit: int = Query(default=20, lte=100),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    supabase = get_supabase_client()
    
    query = supabase.table('journal_entries').select('*').eq('user_id', current_user["id"])
    
    if start_date:
        query = query.gte('created_at', start_date.isoformat())
    
    if end_date:
        query = query.lte('created_at', end_date.isoformat())
    
    # Apply pagination
    query = query.order('created_at', desc=True).range(skip, skip + limit - 1)
    
    response = query.execute()
    return response.data

@router.get("/{entry_id}", response_model=JournalEntryResponse)
async def get_journal_entry(
    entry_id: str,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    response = supabase.table('journal_entries').select('*').eq('id', entry_id).eq('user_id', current_user["id"]).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )
    
    return response.data[0]

@router.put("/{entry_id}", response_model=JournalEntryResponse)
async def update_journal_entry(
    entry_id: str,
    entry_update: JournalEntryUpdate,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    # Check if entry exists and belongs to user
    response = supabase.table('journal_entries').select('*').eq('id', entry_id).eq('user_id', current_user["id"]).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )
    
    # Prepare update data
    update_data = {k: v for k, v in entry_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    # Update the entry
    response = supabase.table('journal_entries').update(update_data).eq('id', entry_id).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update journal entry"
        )
    
    # Re-analyze sentiment if content was updated
    if entry_update.content:
        try:
            sentiment_data = await analyze_sentiment(entry_update.content)
            if sentiment_data:
                supabase.table('journal_entries').update({
                    "sentiment_score": sentiment_data["score"]
                }).eq('id', entry_id).execute()
                response.data[0]["sentiment_score"] = sentiment_data["score"]
        except Exception:
            # Continue even if sentiment analysis fails
            pass
    
    return response.data[0]

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_entry(
    entry_id: str,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    # Check if entry exists and belongs to user
    response = supabase.table('journal_entries').select('*').eq('id', entry_id).eq('user_id', current_user["id"]).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )
    
    # Delete the entry
    supabase.table('journal_entries').delete().eq('id', entry_id).execute()
    
    # No content in response
    return None

@router.get("/{entry_id}/analysis", response_model=JournalAnalysis)
async def analyze_journal_entry(
    entry_id: str,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    # Get the journal entry
    response = supabase.table('journal_entries').select('*').eq('id', entry_id).eq('user_id', current_user["id"]).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )
    
    entry = response.data[0]
    
    # Perform sentiment analysis
    sentiment_data = await analyze_sentiment(entry["content"])
    
    if not sentiment_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sentiment analysis failed"
        )
    
    # Update the entry with sentiment score if it doesn't have one
    if not entry.get("sentiment_score"):
        supabase.table('journal_entries').update({
            "sentiment_score": sentiment_data["score"]
        }).eq('id', entry_id).execute()
    
    return {
        "entry_id": entry_id,
        "sentiment_score": sentiment_data["score"],
        "sentiment_label": sentiment_data["label"],
        "keywords": sentiment_data["keywords"],
        "suggestions": sentiment_data.get("suggestions", [])
    }

@router.get("/")
def list_journals():
    return {"msg": "List journals"}

@router.post("/")
def create_journal():
    return {"msg": "Create journal"}

@router.get("/{journal_id}")
def get_journal(journal_id: int):
    return {"msg": f"Get journal {journal_id}"}

@router.put("/{journal_id}")
def update_journal(journal_id: int):
    return {"msg": f"Update journal {journal_id}"}

@router.delete("/{journal_id}")
def delete_journal(journal_id: int):
    return {"msg": f"Delete journal {journal_id}"} 