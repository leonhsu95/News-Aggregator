"""News API module for fetching articles from NewsAPI and NYT API."""
import requests
from bs4 import BeautifulSoup
from .config import (
    NEWS_API_CATEGORIES, NYT_CATEGORY_MAPPING, USER_AGENT,
    REQUEST_TIMEOUT, ARTICLES_PER_SOURCE, GARBAGE_WORDS, MIN_PARAGRAPH_LENGTH
)


class NewsScraper:
    """Fetches and scrapes news articles from multiple sources."""
    
    def __init__(self, news_key, nyt_key):
        """
        Initialise the scraper with API keys.
        
        Args:
            news_key (str): NewsAPI API key
            nyt_key (str): NYT API key
        """
        self.news_key = news_key
        self.nyt_key = nyt_key
        self.headers = {'User-Agent': USER_AGENT}

    def fetch_all_news(self, category):
        """
        Fetch news from all available sources for a given category.
        
        Args:
            category (str): News category to fetch
            
        Returns:
            list: Combined list of articles from all sources
        """
        all_results = []
        
        # Fetch from NewsAPI if category is supported
        if category in NEWS_API_CATEGORIES:
            news_api_data = self.fetch_news_api(category)
            if isinstance(news_api_data, list):
                all_results.extend(news_api_data)

        # Fetch from NYT API
        nyt_api_data = self.fetch_nyt_api(category)
        if isinstance(nyt_api_data, list):
            all_results.extend(nyt_api_data)
            
        return all_results
    
    def fetch_news_api(self, category):
        """
        Fetch articles from NewsAPI.
        
        Args:
            category (str): News category
            
        Returns:
            list: Articles or error message string
        """
        url = "https://newsapi.org/v2/top-headlines"

        params = {
            'apikey': self.news_key,
            'category': category.lower(),
            'language': 'en',
            'pageSize': ARTICLES_PER_SOURCE
        }

        try:
            response = requests.get(url, params=params)
            articles = response.json().get('articles', [])
            return [
                {
                    'title': a['title'],
                    'source': a['source']['name'],
                    'url': a['url'],
                    'summary': self.scrape_article(a['url'])
                }
                for a in articles
            ]
        
        except Exception as e:
            return f"News API Error: {str(e)}"
        
    def fetch_nyt_api(self, category):
        """
        Fetch articles from New York Times API.
        
        Args:
            category (str): News category
            
        Returns:
            list: Articles or empty list on error
        """
        nyt_cat = NYT_CATEGORY_MAPPING.get(category, "world")
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

        params = {
            'q': nyt_cat,
            'api-key': self.nyt_key
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            docs = data.get('response', {}).get('docs', [])
            
            if not docs:
                return []
            
            return [
                {
                    'title': d['headline']['main'],
                    'source': 'New York Times',
                    'url': d['web_url'],
                    'summary': d.get('abstract', 'No summary available')
                }
                for d in docs[:ARTICLES_PER_SOURCE]
            ]
        
        except Exception as e:
            print(f"NYT Error: {str(e)}")
            return []

    def scrape_article(self, url):
        """
        Scrape article content from URL.
        
        Args:
            url (str): Article URL
            
        Returns:
            str: Article summary or error message
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            valid_paragraphs = []
            
            for p in paragraphs:
                text = p.get_text().strip()
                
                # Filter out short paragraphs
                if len(text) < MIN_PARAGRAPH_LENGTH:
                    continue
                
                # Filter out garbage content
                if any(word in text.lower() for word in GARBAGE_WORDS):
                    continue
                
                valid_paragraphs.append(text)
                
            if valid_paragraphs:
                return "\n\n".join(valid_paragraphs[:5])
            
            return "No summary available!"
            
        except Exception:
            return "Summary extraction failed!"
