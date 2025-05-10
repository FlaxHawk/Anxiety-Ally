from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os
from dotenv import load_dotenv
import logging

from app.config.settings import settings
from app.middleware.rate_limiter import RateLimiter

# Setup logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# For serverless environments
load_dotenv()

app = FastAPI(
    title="Anxiety Ally API",
    description="Backend API for Anxiety Ally mental health platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiter middleware if Redis is configured
if settings.REDIS_URL:
    app.middleware("http")(RateLimiter())

@app.get("/")
async def root():
    return {"message": "Welcome to Anxiety Ally API", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# For AWS Lambda deployment
handler = Mangum(app)

# Import routers after app creation to avoid circular imports
from app.routers import auth, journals, moods, ai

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(journals.router, prefix="/journals", tags=["Journals"])
app.include_router(moods.router, prefix="/moods", tags=["Mood Tracking"])
app.include_router(ai.router, prefix="/ai", tags=["AI Services"]) 