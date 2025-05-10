from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
import hashlib
from typing import Callable, Dict, Optional, Any
import redis
import asyncio
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Rate limiter middleware using Redis for distributed rate limiting
    """
    
    def __init__(
        self,
        redis_url: Optional[str] = None,
        requests: int = 100,
        period: int = 60,
        redis_timeout: int = 3,
    ):
        """
        Initialize the rate limiter
        
        Args:
            redis_url: Redis connection URL
            requests: Maximum number of requests per period
            period: Time period in seconds
            redis_timeout: Redis connection timeout in seconds
        """
        self.redis_url = redis_url or settings.REDIS_URL
        self.requests = requests or settings.RATE_LIMIT_REQUESTS
        self.period = period or settings.RATE_LIMIT_PERIOD
        self.redis_timeout = redis_timeout
        self.redis_client = None
        
        # In-memory fallback cache if Redis is not available
        self.local_cache: Dict[str, Dict[str, Any]] = {}
    
    async def init_redis(self):
        """Initialize Redis connection if URL is available"""
        if not self.redis_url:
            return None
            
        try:
            self.redis_client = redis.from_url(self.redis_url)
            return self.redis_client
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {str(e)}")
            return None
    
    def _get_cache_key(self, request: Request) -> str:
        """
        Generate a unique cache key for the request
        
        Args:
            request: FastAPI request object
            
        Returns:
            String key for the rate limit counter
        """
        # Get client IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.client.host if request.client else "unknown"
        
        # Create key from IP and path
        path = request.url.path
        key_base = f"{ip}:{path}"
        
        # For authenticated users, include user_id if available
        user = getattr(request.state, "user", None)
        if user and hasattr(user, "id"):
            key_base = f"{key_base}:{user.id}"
        
        # Hash the key for privacy
        key = hashlib.md5(key_base.encode()).hexdigest()
        return f"ratelimit:{key}"
    
    async def _redis_check(self, key: str) -> bool:
        """
        Check rate limit using Redis
        
        Args:
            key: Cache key
            
        Returns:
            True if request is allowed, False if rate limited
        """
        pipe = self.redis_client.pipeline()
        
        now = time.time()
        pipe.zremrangebyscore(key, 0, now - self.period)
        pipe.zadd(key, {now: now})
        pipe.zcard(key)
        pipe.expire(key, self.period)
        
        try:
            results = pipe.execute()
            request_count = results[2]
            return request_count <= self.requests
        except Exception as e:
            logger.error(f"Redis error in rate limiter: {str(e)}")
            return True  # Allow request on Redis error
    
    def _local_check(self, key: str) -> bool:
        """
        Check rate limit using local in-memory cache (fallback)
        
        Args:
            key: Cache key
            
        Returns:
            True if request is allowed, False if rate limited
        """
        now = time.time()
        
        # Clean up expired requests
        if key in self.local_cache:
            self.local_cache[key]["timestamps"] = [
                t for t in self.local_cache[key]["timestamps"] if now - t <= self.period
            ]
        else:
            self.local_cache[key] = {"timestamps": []}
        
        # Check count and add new timestamp
        timestamps = self.local_cache[key]["timestamps"]
        if len(timestamps) < self.requests:
            timestamps.append(now)
            return True
        
        return False
    
    async def __call__(self, request: Request, call_next: Callable) -> JSONResponse:
        """
        FastAPI middleware implementation
        
        Args:
            request: FastAPI request object
            call_next: Next middleware or endpoint handler
            
        Returns:
            Response from next handler or rate limit error
        """
        # Skip rate limiting for certain paths
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
            return await call_next(request)
        
        # Initialize Redis if not already connected
        if not self.redis_client and self.redis_url:
            await self.init_redis()
        
        # Get cache key
        key = self._get_cache_key(request)
        
        # Check rate limit
        is_allowed = False
        
        # Try Redis first if available
        if self.redis_client:
            try:
                redis_task = asyncio.create_task(self._redis_check(key))
                is_allowed = await asyncio.wait_for(redis_task, timeout=self.redis_timeout)
            except (asyncio.TimeoutError, Exception) as e:
                logger.warning(f"Redis rate limit check failed, using local cache: {str(e)}")
                is_allowed = self._local_check(key)
        else:
            # Fallback to local cache
            is_allowed = self._local_check(key)
        
        if not is_allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": f"Rate limit exceeded: {self.requests} requests per {self.period} seconds"}
            )
        
        return await call_next(request) 