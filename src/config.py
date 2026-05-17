"""Configuration module for API keys and settings."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NYT_API_KEY = os.getenv("NYT_API_KEY")

# Categories supported by NewsAPI
NEWS_API_CATEGORIES = ['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology']

# All available categories (includes NYT-only categories)
ALL_CATEGORIES = ['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology', 
                  'Fashion', 'Food', 'Travel', 'RealEstate', 'Politics']

# Category mapping for NYT API
NYT_CATEGORY_MAPPING = {
    "General": "world",
    "Entertainment": "arts",
    "Business": "business",
    "Technology": "technology",
    "Science": "science",
    "Health": "health",
    "Sports": "sports",
    "Fashion": "fashion",
    "Food": "dining",
    "Travel": "travel",
    "RealEstate": "realestate",
    "Politics": "politics"
}

# Web scraper settings
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
REQUEST_TIMEOUT = 5
ARTICLES_PER_SOURCE = 10

# Garbage words to filter out summaries
GARBAGE_WORDS = ['advertisement', 'subscribe', 'sign up', 'cookie', 'privacy policy', 
                 'terms of service', 'javascript', 'browser version', 'enable cookies', 'support for css']

# Minimum paragraph length for valid content
MIN_PARAGRAPH_LENGTH = 50


def validate_keys():
    """Validate that API keys are available."""
    if not NEWS_API_KEY:
        print("⚠️  NewsAPI Key NOT found.")
        return False
    
    if not NYT_API_KEY:
        print("⚠️  NYT API Key NOT found.")
        return False
    
    print("✓ NewsAPI Key found!")
    print("✓ NYT API Key found!")
    return True
