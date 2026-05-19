"""Main entry point for the News Aggregator application."""
import streamlit as st
from .config import NEWS_API_KEY, NYT_API_KEY, validate_keys
from .api import NewsScraper
from .ui import run_app


def main():
    """Launch the News Aggregator application."""
    # Validate API keys before starting
    if not validate_keys():
        st.error("Error: API keys not configured. Please set NEWS_API_KEY and NYT_API_KEY in .env")
        return

    try:
        # Create news scraper and run the app
        news_engine = NewsScraper(NEWS_API_KEY, NYT_API_KEY)
        run_app(news_engine)

    except Exception as e:
        st.error(f"App error: {e}")


if __name__ == "__main__":
    main()
