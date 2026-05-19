"""Tests for the config module."""
import unittest
from unittest.mock import patch
from src import config


class TestConfig(unittest.TestCase):
    """Test cases for config module."""
    
    def test_api_categories_list(self):
        """Test that API categories are defined."""
        self.assertIsInstance(config.NEWS_API_CATEGORIES, list)
        self.assertIn('Business', config.NEWS_API_CATEGORIES)
        self.assertIn('Technology', config.NEWS_API_CATEGORIES)
    
    def test_all_categories_list(self):
        """Test that all categories list includes more than NewsAPI categories."""
        self.assertGreaterEqual(len(config.ALL_CATEGORIES), len(config.NEWS_API_CATEGORIES))
        self.assertIn('Fashion', config.ALL_CATEGORIES)
        self.assertIn('Politics', config.ALL_CATEGORIES)
    
    def test_nyt_category_mapping(self):
        """Test NYT category mapping."""
        self.assertEqual(config.NYT_CATEGORY_MAPPING['Business'], 'business')
        self.assertEqual(config.NYT_CATEGORY_MAPPING['Entertainment'], 'arts')
        self.assertEqual(config.NYT_CATEGORY_MAPPING['Food'], 'dining')
    
    def test_garbage_words_defined(self):
        """Test that garbage words filter is defined."""
        self.assertIsInstance(config.GARBAGE_WORDS, list)
        self.assertGreater(len(config.GARBAGE_WORDS), 0)
        self.assertIn('advertisement', config.GARBAGE_WORDS)
    
    def test_min_paragraph_length_defined(self):
        """Test minimum paragraph length is configured."""
        self.assertGreater(config.MIN_PARAGRAPH_LENGTH, 0)
        self.assertEqual(config.MIN_PARAGRAPH_LENGTH, 50)
    
    def test_user_agent_defined(self):
        """Test that user agent string is defined."""
        self.assertIsInstance(config.USER_AGENT, str)
        self.assertGreater(len(config.USER_AGENT), 0)
        self.assertIn('Mozilla', config.USER_AGENT)
