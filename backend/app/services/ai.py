import httpx
import json
from typing import Dict, Any, Optional, List
import os
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)

async def analyze_sentiment(text: str) -> Optional[Dict[str, Any]]:
    """
    Analyzes the sentiment of a text using Hugging Face API
    
    Args:
        text: The text to analyze
        
    Returns:
        Dict with sentiment analysis results or None if failed
    """
    if not settings.HUGGINGFACE_API_KEY:
        logger.warning("Hugging Face API key not set, skipping sentiment analysis")
        # Return mock data for development without API key
        return {
            "score": 0.75,
            "label": "POSITIVE",
            "keywords": ["happy", "good", "better"],
        }
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # Using distilbert-base-uncased-finetuned-sst-2-english for sentiment
            payload = {
                "inputs": text[:512]  # Limit text length
            }
            
            response = await client.post(
                "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
                headers=headers,
                json=payload,
                timeout=10.0
            )
            
            if response.status_code != 200:
                logger.error(f"Hugging Face API error: {response.text}")
                return None
            
            sentiment_data = response.json()
            
            # Extract keywords using textrank algorithm (simplified version)
            keywords = extract_keywords(text)
            
            # Build result
            if isinstance(sentiment_data, list) and len(sentiment_data) > 0:
                result = {
                    "score": next((item["score"] for item in sentiment_data if item["label"] == "POSITIVE"), 0.5),
                    "label": sentiment_data[0]["label"],
                    "keywords": keywords
                }
                
                # Generate suggestions based on sentiment
                if result["label"] == "NEGATIVE" and result["score"] < 0.3:
                    result["suggestions"] = [
                        "Consider practicing deep breathing for 5 minutes",
                        "Try to identify specific triggers for these feelings",
                        "Remember a time you felt more positive about this situation"
                    ]
                
                return result
            
            return None
            
    except Exception as e:
        logger.exception(f"Error during sentiment analysis: {str(e)}")
        return None

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """
    Simple keyword extraction function
    In a production system, you would use a proper NLP library like spaCy or NLTK
    
    Args:
        text: The text to extract keywords from
        max_keywords: Maximum number of keywords to extract
        
    Returns:
        List of extracted keywords
    """
    # This is a very simplified version
    # In production, use TextRank or similar algorithms
    words = text.lower().split()
    
    # Remove stopwords (very basic list)
    stopwords = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", 
                "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", 
                "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", 
                "their", "theirs", "themselves", "what", "which", "who", "whom", "this", 
                "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", 
                "being", "have", "has", "had", "having", "do", "does", "did", "doing", 
                "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", 
                "while", "of", "at", "by", "for", "with", "about", "against", "between", 
                "into", "through", "during", "before", "after", "above", "below", "to", 
                "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", 
                "further", "then", "once", "here", "there", "when", "where", "why", "how", 
                "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", 
                "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", 
                "t", "can", "will", "just", "don", "should", "now"}
    
    filtered_words = [word for word in words if word not in stopwords and len(word) > 3]
    
    # Count word frequency
    word_freq = {}
    for word in filtered_words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Return top keywords
    return [word for word, _ in sorted_words[:max_keywords]]

async def chat_with_bot(message: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Chat with the CBT bot using Hugging Face API
    
    Args:
        message: User message
        history: Chat history as list of {"role": "user"|"assistant", "content": "message"}
        
    Returns:
        Dict with response from the chatbot
    """
    if not settings.HUGGINGFACE_API_KEY:
        logger.warning("Hugging Face API key not set, using mock chatbot response")
        return {
            "response": "I'm here to help you with cognitive behavioral therapy techniques. " +
                      "What are you feeling right now?",
            "suggestions": ["Tell me more about that feeling", 
                           "When did you start feeling this way?",
                           "What thoughts are associated with this feeling?"]
        }
    
    try:
        # Prepare conversation history
        if not history:
            history = []
        
        # Add system message if not present
        if not any(msg.get("role") == "system" for msg in history):
            history.insert(0, {
                "role": "system",
                "content": "You are a helpful assistant trained in cognitive behavioral therapy (CBT). " +
                         "Your goal is to help users identify negative thought patterns and develop " +
                         "healthier thinking habits. Be empathetic and supportive, but also help " +
                         "users challenge distorted thoughts."
            })
        
        # Add user message
        history.append({
            "role": "user",
            "content": message
        })
        
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # For production, consider using a model specifically fine-tuned for CBT
            # Here we're using a general model
            response = await client.post(
                "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
                headers=headers,
                json={"inputs": history},
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Hugging Face API error: {response.text}")
                return {
                    "response": "I'm sorry, I'm having trouble processing your request right now. Please try again later.",
                    "suggestions": ["How are you feeling right now?", 
                                  "Would you like to try a different approach?",
                                  "Let's take a deep breath together."]
                }
            
            bot_response = response.json()
            
            # Process response from the model
            assistant_message = bot_response.get("generated_text", "")
            
            # Generate follow-up suggestions based on common CBT techniques
            suggestions = [
                "What evidence supports this thought?",
                "Is there another way to look at this situation?",
                "What would you tell a friend who was in this situation?"
            ]
            
            return {
                "response": assistant_message,
                "suggestions": suggestions
            }
            
    except Exception as e:
        logger.exception(f"Error during chatbot interaction: {str(e)}")
        return {
            "response": "I apologize, but I encountered an error. Please try again later.",
            "suggestions": ["Let's try a different approach", "How are you feeling right now?"]
        } 