from supabase import create_client, Client
from app.config.settings import settings
import httpx

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client instance
    
    Returns:
        Client: A configured Supabase client
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Supabase URL and key must be provided in environment variables")
    
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return client

async def healthcheck_supabase() -> bool:
    """
    Checks if Supabase is available and responding
    
    Returns:
        bool: True if Supabase is healthy, False otherwise
    """
    try:
        # Using httpx to make a simple request to Supabase health endpoint
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.SUPABASE_URL}/rest/v1/?apikey={settings.SUPABASE_KEY}")
            return response.status_code == 200
    except Exception:
        return False 