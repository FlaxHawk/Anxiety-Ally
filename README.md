# Anxiety Ally

A web platform designed to help users manage anxiety and improve mental health through mood tracking, journaling, and guided exercises.

## Project Overview

Anxiety Ally is a comprehensive mental health companion that provides users with tools to:

- Track daily moods and identify emotional patterns
- Journal thoughts and feelings with AI-powered sentiment analysis
- Practice guided breathing exercises designed to reduce anxiety
- Chat with a CBT-trained assistant for personalized support
- Join community forums for peer support and shared experiences

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT-based authentication
- **AI Services**: Hugging Face Inference API
- **Deployment**: Serverless architecture (AWS Lambda or Vercel Functions)

### Frontend
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS
- **State Management**: React Query and Context API
- **Form Handling**: React Hook Form with Zod validation
- **Animations**: Framer Motion
- **Deployment**: Vercel

## Project Structure

```
anxiety-ally/
├── backend/              # FastAPI backend
│   ├── app/              # Application code
│   │   ├── config/       # Configuration settings
│   │   ├── middleware/   # API middleware
│   │   ├── models/       # Data models
│   │   ├── routers/      # API routes
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # External services
│   └── tests/            # Backend tests
├── frontend/             # Next.js frontend
│   ├── app/              # App router
│   ├── components/       # Reusable components
│   ├── lib/              # Utilities and hooks
│   └── public/           # Static assets
└── README.md             # Project documentation
```

## Features

### Mood Tracking
- Daily mood recording with customizable notes
- Visual charts to identify patterns over time
- Historical mood data with filtering options

### Journaling
- Rich text editor for detailed expression
- AI-powered sentiment analysis of entries
- Customizable tags and media attachment support

### Breathing Exercises
- Guided interactive breathing patterns
- Visual animations to assist with proper technique
- Various exercise types for different situations

### CBT Chatbot
- Cognitive Behavioral Therapy techniques
- Personalized suggestions based on user input
- Helpful follow-up prompts for self-reflection

### Community Support (Future)
- Moderated discussion forums
- Anonymous sharing options
- Topic-based organization

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Supabase account
- Hugging Face API key (for AI features)

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - MacOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with required environment variables (see `.env.example`)
6. Run the API: `uvicorn app.main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Create a `.env.local` file with required environment variables (see `.env.example`)
4. Run the development server: `npm run dev`
5. Access the app at `http://localhost:3000`

## Deployment

### Backend Deployment
- The backend is designed to be deployed as a serverless function on AWS Lambda or similar services
- The included `Dockerfile` can also be used for containerized deployment

### Frontend Deployment
- The frontend is optimized for deployment on Vercel
- Simply connect your GitHub repository to Vercel for automatic deployments

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by mental health professionals and resources
- Uses open-source AI models from Hugging Face
- Built with accessibility and inclusivity in mind 