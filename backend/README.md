# Anxiety Ally Backend

The backend service for the Anxiety Ally application built with FastAPI and Supabase.

## Dependency Resolution and Python 3.13

The project has dependencies that are not fully compatible with Python 3.13 due to the following issues:

1. OpenTelemetry packages have conflicting semantic-conventions dependencies
2. Pydantic has compatibility issues with Python 3.13
3. Type annotation and forward reference handling differences in Python 3.13

To resolve these issues, we recommend using Docker with Python 3.10, which is known to be compatible with all dependencies.

## Setup with Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed

2. Create a `.env` file with necessary configuration

3. Build and start the containers:
```bash
docker-compose up -d
```

The API will be available at http://localhost:8000

## Alternative: Local Python Setup

If you prefer to run without Docker, you need Python 3.10:

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with necessary configuration (see `.env.example` if available).

5. Start the development server:
```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Project Structure

```
app/
├── config/        # Configuration settings
├── middleware/    # Middleware components (auth, rate limiting)
├── models/        # Data models and schemas
├── routers/       # API route definitions
├── schemas/       # Pydantic schemas for validation
├── services/      # Business logic
└── main.py        # Application entry point
``` 