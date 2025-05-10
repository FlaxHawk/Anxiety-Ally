from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

from app.config.settings import settings
from app.schemas.auth import Token, TokenData, UserCreate, UserResponse
from app.services.supabase import get_supabase_client

router = APIRouter(prefix="/auth", tags=["auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# User authentication
async def authenticate_user(email: str, password: str):
    supabase = get_supabase_client()
    response = supabase.table('users').select('*').eq('email', email).execute()
    
    if len(response.data) == 0:
        return False
    
    user = response.data[0]
    if not pwd_context.verify(password, user['password']):
        return False
    
    return user

# Get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    supabase = get_supabase_client()
    response = supabase.table('users').select('*').eq('id', token_data.user_id).execute()
    
    if len(response.data) == 0:
        raise credentials_exception
        
    return response.data[0]

@router.post("/register")
def register():
    return {"msg": "Register endpoint"}

@router.post("/login")
def login():
    return {"msg": "Login endpoint"}

@router.get("/profile")
def profile():
    return {"msg": "Profile endpoint"}

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    supabase = get_supabase_client()
    
    # Check if user already exists
    existing_user = supabase.table('users').select('*').eq('email', user.email).execute()
    if len(existing_user.data) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Create the user in Supabase
    new_user = {
        "email": user.email,
        "password": hashed_password,
        "full_name": user.full_name,
        "created_at": datetime.utcnow().isoformat()
    }
    
    response = supabase.table('users').insert(new_user).execute()
    
    if len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    created_user = response.data[0]
    return {
        "id": created_user["id"],
        "email": created_user["email"],
        "full_name": created_user["full_name"]
    }

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_user_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "full_name": current_user["full_name"]
    } 