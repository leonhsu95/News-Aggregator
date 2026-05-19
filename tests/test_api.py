"""Tests for the API module."""
import unittest
from unittest.mock import patch, MagicMock
from src.api import NewsScraper


class TestNewsScraper(unittest.TestCase):
    """Test cases for NewsScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = NewsScraper("test_news_key", "test_nyt_key")
    
    def test_fetch_news_api_success(self):
        """Test successful fetch from NewsAPI."""
        mock_response = {
            'articles': [
                {
                    'title': 'Test Article',
                    'source': {'name': 'Test Source'},
                    'url': 'https://example.com/article1'
                }
            ]
        }
        
        with patch('src.api.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            
            with patch.object(self.scraper, 'scrape_article', return_value='Test summary'):
                result = self.scraper.fetch_news_api('Technology')
            
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['title'], 'Test Article')
            self.assertEqual(result[0]['source'], 'Test Source')
    
    def test_fetch_news_api_error(self):
        """Test error handling in NewsAPI."""
        with patch('src.api.requests.get', side_effect=Exception("Connection failed")):
            result = self.scraper.fetch_news_api('Technology')
        
        self.assertIsInstance(result, str)
        self.assertIn("Error", result)
    
    def test_fetch_nyt_api_success(self):
        """Test successful fetch from NYT API."""
        mock_response = {
            'response': {
                'docs': [
                    {
                        'headline': {'main': 'NYT Article'},
                        'web_url': 'https://nytimes.com/article1',
                        'abstract': 'Test abstract'
                    }
                ]
            }
        }
        
        with patch('src.api.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            result = self.scraper.fetch_nyt_api('Business')
            
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['title'], 'NYT Article')
            self.assertEqual(result[0]['source'], 'New York Times')
    
    def test_fetch_nyt_api_empty(self):
        """Test NYT API with no results."""
        mock_response = {'response': {'docs': []}}
        
        with patch('src.api.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            result = self.scraper.fetch_nyt_api('Business')
            
            self.assertEqual(result, [])
    
    def test_scrape_article_success(self):
        """Test article scraping success."""
        html_content = """
        <html>
            <body>
                <p>This is a long paragraph with more than fifty characters for testing.</p>
                <p>Another paragraph with more than fifty characters in it as well.</p>
            </body>
        </html>
        """
        
        with patch('src.api.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.content = html_content.encode()
            mock_get.return_value = mock_response
            
            result = self.scraper.scrape_article('https://example.com/article')
            
            self.assertIn('long paragraph', result)
            self.assertNotEqual(result, "Summary extraction failed!")


def test_scrape_article_failure(scraper):
    """Test article scraping failure handling."""
    with patch('src.api.requests.get', side_effect=Exception("Network error")):
        result = scraper.scrape_article('https://example.com/article')
    
    assert result == "Summary extraction failed!"


def test_fetch_all_news_combines_sources(scraper):
    """Test that fetch_all_news combines results from both sources."""
    news_api_result = [{'title': 'NewsAPI Article', 'source': 'NewsAPI', 'url': 'https://newsapi.org', 'summary': 'summary1'}]
    nyt_result = [{'title': 'NYT Article', 'source': 'NYT', 'url': 'https://nyt.com', 'summary': 'summary2'}]
    
    with patch.object(scraper, 'fetch_news_api', return_value=news_api_result):
        with patch.object(scraper, 'fetch_nyt_api', return_value=nyt_result):
            result = scraper.fetch_all_news('Business')
    
    assert len(result) == 2
    assert any(article['source'] == 'NewsAPI' for article in result)
    assert any(article['source'] == 'NYT' for article in result)
