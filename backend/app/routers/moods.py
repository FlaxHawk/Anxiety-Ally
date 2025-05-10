from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timedelta, date
import statistics

from app.schemas.moods import MoodCreate, MoodUpdate, MoodResponse, MoodAggregation
from app.routers.auth import get_current_user
from app.services.supabase import get_supabase_client

router = APIRouter(prefix="/moods", tags=["moods"])

@router.post("/", response_model=MoodResponse)
async def create_mood(
    mood: MoodCreate,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    new_mood = {
        "score": mood.score,
        "notes": mood.notes,
        "user_id": current_user["id"],
        "timestamp": (mood.timestamp or datetime.utcnow()).isoformat(),
        "created_at": datetime.utcnow().isoformat()
    }
    
    response = supabase.table('moods').insert(new_mood).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create mood entry"
        )
    
    return response.data[0]

@router.get("/", response_model=List[MoodResponse])
async def get_moods(
    current_user = Depends(get_current_user),
    skip: int = 0,
    limit: int = Query(default=20, lte=100),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    supabase = get_supabase_client()
    
    query = supabase.table('moods').select('*').eq('user_id', current_user["id"])
    
    if start_date:
        query = query.gte('timestamp', start_date.isoformat())
    
    if end_date:
        query = query.lte('timestamp', end_date.isoformat())
    
    # Apply pagination and sorting
    query = query.order('timestamp', desc=True).range(skip, skip + limit - 1)
    
    response = query.execute()
    return response.data

@router.get("/{mood_id}", response_model=MoodResponse)
async def get_mood(
    mood_id: str,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    response = supabase.table('moods').select('*').eq('id', mood_id).eq('user_id', current_user["id"]).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mood entry not found"
        )
    
    return response.data[0]

@router.put("/{mood_id}", response_model=MoodResponse)
async def update_mood(
    mood_id: str,
    mood_update: MoodUpdate,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    # Check if mood exists and belongs to user
    response = supabase.table('moods').select('*').eq('id', mood_id).eq('user_id', current_user["id"]).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mood entry not found"
        )
    
    # Prepare update data
    update_data = {k: v for k, v in mood_update.dict().items() if v is not None}
    
    # Update the mood
    response = supabase.table('moods').update(update_data).eq('id', mood_id).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update mood entry"
        )
    
    return response.data[0]

@router.delete("/{mood_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mood(
    mood_id: str,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    # Check if mood exists and belongs to user
    response = supabase.table('moods').select('*').eq('id', mood_id).eq('user_id', current_user["id"]).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mood entry not found"
        )
    
    # Delete the mood
    supabase.table('moods').delete().eq('id', mood_id).execute()
    
    # No content in response
    return None

@router.get("/aggregate/{period}", response_model=MoodAggregation)
async def aggregate_moods(
    period: str,
    current_user = Depends(get_current_user),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    if period not in ["day", "week", "month"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Period must be one of: day, week, month"
        )
    
    # Set default date range if not provided
    today = date.today()
    if not end_date:
        end_date = today
    
    if not start_date:
        if period == "day":
            start_date = end_date - timedelta(days=7)  # Last week
        elif period == "week":
            start_date = end_date - timedelta(weeks=4)  # Last 4 weeks
        else:  # month
            start_date = end_date - timedelta(days=90)  # Last 3 months
    
    supabase = get_supabase_client()
    
    # Get all moods in the date range
    response = supabase.table('moods') \
        .select('*') \
        .eq('user_id', current_user["id"]) \
        .gte('timestamp', datetime.combine(start_date, datetime.min.time()).isoformat()) \
        .lte('timestamp', datetime.combine(end_date, datetime.max.time()).isoformat()) \
        .execute()
    
    if len(response.data) == 0:
        return {
            "period": period,
            "data": [],
            "average_score": 0
        }
    
    # Process data based on period
    aggregated_data = {}
    
    for mood in response.data:
        mood_date = datetime.fromisoformat(mood["timestamp"].replace("Z", "+00:00")).date()
        
        if period == "day":
            key = mood_date.isoformat()
        elif period == "week":
            # Get the Monday of the week
            week_start = mood_date - timedelta(days=mood_date.weekday())
            key = week_start.isoformat()
        else:  # month
            key = f"{mood_date.year}-{mood_date.month:02d}"
        
        if key not in aggregated_data:
            aggregated_data[key] = []
        
        aggregated_data[key].append(mood["score"])
    
    # Calculate averages for each period
    result_data = []
    for key, scores in aggregated_data.items():
        avg_score = statistics.mean(scores)
        result_data.append({
            "period": key,
            "average_score": round(avg_score, 2),
            "count": len(scores)
        })
    
    # Sort by period
    result_data.sort(key=lambda x: x["period"])
    
    # Calculate overall average
    all_scores = [mood["score"] for mood in response.data]
    overall_average = statistics.mean(all_scores) if all_scores else 0
    
    return {
        "period": period,
        "data": result_data,
        "average_score": round(overall_average, 2)
    }

@router.get("/")
def list_moods():
    return {"msg": "List moods"}

@router.post("/")
def create_mood():
    return {"msg": "Create mood"} 